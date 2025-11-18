import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader, Check, CheckCheck, Smile, Paperclip, MoreVertical, Phone, Video, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { socket } from '../lib/socket';
import { useAuthStore } from '../store/authStore';

/**
 * Enhanced Messaging Panel Component
 *
 * Features:
 * - Real-time message delivery with smooth animations
 * - Enhanced typing indicators with dots animation
 * - Read receipts with visual feedback
 * - Message batching and grouping by date
 * - Optimistic UI updates
 * - Automatic reconnection with status indicators
 * - Modern, polished UI design
 * - Message timestamps on hover
 * - Smooth scroll animations
 */

interface Message {
  id: string;
  conversationId: string;
  senderId: string;
  recipientId: string;
  content: string;
  type: 'text' | 'system' | 'introduction' | 'proposal';
  status: 'sent' | 'delivered' | 'read';
  createdAt: Date;
  deliveredAt?: Date;
  readAt?: Date;
}

interface Conversation {
  id: string;
  participants: string[];
  type: 'direct' | 'negotiation' | 'introduction';
  lastMessage?: Message;
  unreadCount: number;
}

interface MessagingPanelProps {
  conversationId?: string;
  recipientId?: string;
  recipientName?: string;
}

export function MessagingPanel({ conversationId, recipientId, recipientName }: MessagingPanelProps) {
  const { user } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isConnected, setIsConnected] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    function onConnect() {
      setIsConnected(true);

      // Request message history if conversation exists
      if (conversationId) {
        socket.emit('messages:history', {
          conversationId,
          limit: 50
        });
      }
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    function onMessagesHistory(data: { conversationId: string; messages: any[] }) {
      if (data.conversationId === conversationId) {
        setMessages(data.messages.map(m => ({
          ...m,
          createdAt: new Date(m.created_at),
          deliveredAt: m.delivered_at ? new Date(m.delivered_at) : undefined,
          readAt: m.read_at ? new Date(m.read_at) : undefined
        })));
      }
    }

    function onNewMessage(message: any) {
      if (message.conversationId === conversationId) {
        setMessages(prev => [...prev, {
          ...message,
          createdAt: new Date(message.createdAt),
          deliveredAt: message.deliveredAt ? new Date(message.deliveredAt) : undefined,
          readAt: message.readAt ? new Date(message.readAt) : undefined
        }]);

        // Send read receipt if we're the recipient
        if (message.recipientId === user?.id) {
          socket.emit('message:read', { messageId: message.id });
        }

        // Scroll to bottom
        scrollToBottom();
      }
    }

    function onMessageSent(data: { tempId?: string; message: any }) {
      // Replace optimistic message with real one
      const realMessage = {
        ...data.message,
        createdAt: new Date(data.message.createdAt),
        deliveredAt: data.message.deliveredAt ? new Date(data.message.deliveredAt) : undefined,
        readAt: data.message.readAt ? new Date(data.message.readAt) : undefined
      };

      if (data.tempId) {
        setMessages(prev => prev.map(m =>
          m.id === data.tempId ? realMessage : m
        ));
      }

      setIsSending(false);
    }

    function onTypingUpdate(data: { userId: string; isTyping: boolean }) {
      if (data.userId === recipientId) {
        setIsTyping(data.isTyping);
      }
    }

    function onMessageRead(data: { messageId: string }) {
      setMessages(prev => prev.map(m =>
        m.id === data.messageId ? { ...m, status: 'read' as const, readAt: new Date() } : m
      ));
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('messages:history', onMessagesHistory);
    socket.on('message:new', onNewMessage);
    socket.on('message:sent', onMessageSent);
    socket.on('typing:update', onTypingUpdate);
    socket.on('message:read', onMessageRead);

    if (!socket.connected) {
      socket.connect();
    }

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('messages:history', onMessagesHistory);
      socket.off('message:new', onNewMessage);
      socket.off('message:sent', onMessageSent);
      socket.off('typing:update', onTypingUpdate);
      socket.off('message:read', onMessageRead);
    };
  }, [conversationId, recipientId, user?.id]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = () => {
    if (!inputValue.trim() || !recipientId) return;

    // Optimistic update
    const tempId = `temp-${Date.now()}`;
    const optimisticMessage: Message = {
      id: tempId,
      conversationId: conversationId || '',
      senderId: user!.id,
      recipientId,
      content: inputValue,
      type: 'text',
      status: 'sent',
      createdAt: new Date()
    };

    setMessages(prev => [...prev, optimisticMessage]);
    setIsSending(true);

    // Send via socket
    socket.emit('message:send', {
      conversationId,
      recipientId,
      content: inputValue,
      type: 'text',
      metadata: { tempId }
    });

    setInputValue('');
    scrollToBottom();

    // Stop typing indicator
    socket.emit('typing:stop', { conversationId });
  };

  const handleInputChange = (value: string) => {
    setInputValue(value);

    // Clear previous timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Start typing indicator
    if (value.length > 0 && conversationId) {
      socket.emit('typing:start', { conversationId });

      // Auto-stop after 3 seconds of inactivity
      typingTimeoutRef.current = setTimeout(() => {
        socket.emit('typing:stop', { conversationId });
      }, 3000);
    } else if (conversationId) {
      socket.emit('typing:stop', { conversationId });
    }
  };

  const getMessageStatusIcon = (message: Message) => {
    if (message.senderId !== user?.id) return null;

    if (message.status === 'read') {
      return <CheckCheck className="w-3 h-3 text-blue-400" />;
    } else if (message.status === 'delivered') {
      return <CheckCheck className="w-3 h-3 text-gray-400" />;
    } else {
      return <Check className="w-3 h-3 text-gray-400" />;
    }
  };

  const formatMessageDate = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return date.toLocaleDateString('en-US', { weekday: 'long' });
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const groupMessagesByDate = (messages: Message[]) => {
    const groups: { [key: string]: Message[] } = {};

    messages.forEach(message => {
      const dateKey = message.createdAt.toDateString();
      if (!groups[dateKey]) {
        groups[dateKey] = [];
      }
      groups[dateKey].push(message);
    });

    return Object.entries(groups).map(([date, msgs]) => ({
      date: new Date(date),
      messages: msgs
    }));
  };

  const messageGroups = groupMessagesByDate(messages);

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-gray-50 to-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden">
      {/* Enhanced Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                {recipientName?.charAt(0).toUpperCase() || 'C'}
              </div>
              <div className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${isConnected ? 'bg-green-500' : 'bg-gray-400'}`} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{recipientName || 'Conversation'}</h3>
              <AnimatePresence mode="wait">
                {isTyping ? (
                  <motion.div
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    className="flex items-center gap-1 text-xs text-blue-600"
                  >
                    <span>typing</span>
                    <motion.span
                      animate={{ opacity: [1, 0.4, 1] }}
                      transition={{ duration: 1, repeat: Infinity }}
                    >
                      ...
                    </motion.span>
                  </motion.div>
                ) : (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-xs text-gray-500"
                  >
                    {isConnected ? 'Active now' : 'Connecting...'}
                  </motion.p>
                )}
              </AnimatePresence>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <Phone className="w-5 h-5 text-gray-600" />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <Video className="w-5 h-5 text-gray-600" />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <Info className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>
      </div>

      {/* Enhanced Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-6 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
        {messageGroups.map((group, groupIndex) => (
          <div key={groupIndex} className="space-y-4">
            {/* Date Separator */}
            <div className="flex items-center justify-center">
              <div className="bg-gray-200 text-gray-600 text-xs font-medium px-3 py-1 rounded-full">
                {formatMessageDate(group.date)}
              </div>
            </div>

            {/* Messages in group */}
            <AnimatePresence>
              {group.messages.map((message, index) => {
                const isOwnMessage = message.senderId === user?.id;
                const showAvatar = index === 0 || group.messages[index - 1]?.senderId !== message.senderId;

                return (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className={`flex gap-2 ${isOwnMessage ? 'justify-end' : 'justify-start'}`}
                  >
                    {!isOwnMessage && (
                      <div className="flex-shrink-0 w-8">
                        {showAvatar && (
                          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center text-white text-xs font-semibold">
                            {recipientName?.charAt(0).toUpperCase() || 'U'}
                          </div>
                        )}
                      </div>
                    )}

                    <div
                      className={`group max-w-[70%] ${
                        isOwnMessage ? 'items-end' : 'items-start'
                      } flex flex-col gap-1`}
                    >
                      <div
                        className={`relative px-4 py-2.5 rounded-2xl shadow-sm transition-all ${
                          isOwnMessage
                            ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-br-sm'
                            : 'bg-white border border-gray-200 text-gray-900 rounded-bl-sm'
                        }`}
                      >
                        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                          {message.content}
                        </p>
                      </div>

                      {/* Timestamp and Status */}
                      <div
                        className={`flex items-center gap-1.5 px-2 opacity-0 group-hover:opacity-100 transition-opacity ${
                          isOwnMessage ? 'flex-row-reverse' : 'flex-row'
                        }`}
                      >
                        <span className="text-xs text-gray-500">
                          {message.createdAt.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                        {getMessageStatusIcon(message)}
                      </div>
                    </div>

                    {isOwnMessage && <div className="flex-shrink-0 w-8" />}
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex items-end gap-3">
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors mb-1">
            <Paperclip className="w-5 h-5 text-gray-600" />
          </button>

          <div className="flex-1 relative">
            <textarea
              value={inputValue}
              onChange={(e) => handleInputChange(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Type a message..."
              rows={1}
              className="w-full px-4 py-3 pr-12 bg-gray-100 border-0 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white resize-none transition-all placeholder:text-gray-500"
              style={{ minHeight: '48px', maxHeight: '120px' }}
              disabled={!isConnected || isSending}
            />
            <button className="absolute right-3 bottom-3 p-1 hover:bg-gray-200 rounded-lg transition-colors">
              <Smile className="w-5 h-5 text-gray-600" />
            </button>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || !isConnected || isSending}
            className={`p-3 rounded-xl transition-all shadow-md mb-1 ${
              inputValue.trim() && isConnected && !isSending
                ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white hover:shadow-lg'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            {isSending ? (
              <Loader className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </motion.button>
        </div>

        {!isConnected && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 text-xs text-red-500 flex items-center gap-1"
          >
            <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
            Reconnecting to chat...
          </motion.div>
        )}
      </div>
    </div>
  );
}
