import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageCircle,
  X,
  Send,
  Sparkles,
  Minimize2,
  User,
  Bot,
} from 'lucide-react';
import { chatbotApi } from '../lib/api';
import { useAuthStore } from '../store/authStore';
import type { ChatMessage } from '../types';
import { cn, generateId } from '../lib/utils';

const WELCOME_MESSAGES = [
  "Hi there! 👋 I'm Bond, your AI assistant. How can I help you today?",
  "Welcome to Bond.AI! I'm here to help you navigate and make the most of your connections.",
  "Hello! Looking to build meaningful partnerships? I'm here to guide you!",
];

const SUGGESTED_QUESTIONS = [
  "How does AI matching work?",
  "How do I add my needs and offerings?",
  "What makes a good match?",
  "How does agent-to-agent negotiation work?",
];

export default function ChatbotWidget() {
  const { isAuthenticated } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: generateId(),
      role: 'assistant',
      content: WELCOME_MESSAGES[Math.floor(Math.random() * WELCOME_MESSAGES.length)],
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isTyping) return;

    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await chatbotApi.sendMessage(input, {
        isAuthenticated,
        currentPath: window.location.pathname,
      });

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: "I apologize, but I'm having trouble connecting right now. Please try again in a moment!",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSuggestedQuestion = (question: string) => {
    setInput(question);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-accent rounded-full shadow-2xl flex items-center justify-center hover:shadow-primary-500/50 transition-shadow z-50 group"
          >
            <MessageCircle className="w-7 h-7 text-white group-hover:scale-110 transition-transform" />
            <motion.div
              className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className={cn(
              "fixed bottom-6 right-6 w-96 bg-white rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden",
              isMinimized ? "h-16" : "h-[600px]"
            )}
          >
            {/* Header */}
            <div className="bg-gradient-accent text-white px-5 py-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                  <Sparkles className="w-6 h-6" />
                </div>
                <div>
                  <div className="font-semibold">Bond Assistant</div>
                  <div className="text-xs text-white/80">
                    {isTyping ? 'Typing...' : 'Online'}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setIsMinimized(!isMinimized)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <Minimize2 className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {!isMinimized && (
              <>
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={cn(
                        "flex items-start space-x-2",
                        message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      )}
                    >
                      <div
                        className={cn(
                          "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                          message.role === 'user'
                            ? 'bg-primary-600'
                            : 'bg-gradient-accent'
                        )}
                      >
                        {message.role === 'user' ? (
                          <User className="w-5 h-5 text-white" />
                        ) : (
                          <Bot className="w-5 h-5 text-white" />
                        )}
                      </div>

                      <div
                        className={cn(
                          "max-w-[75%] rounded-2xl px-4 py-2.5",
                          message.role === 'user'
                            ? 'bg-primary-600 text-white'
                            : 'bg-white text-gray-900 shadow-sm'
                        )}
                      >
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {message.content}
                        </p>
                      </div>
                    </div>
                  ))}

                  {isTyping && (
                    <div className="flex items-start space-x-2">
                      <div className="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                      </div>
                      <div className="bg-white rounded-2xl px-4 py-3 shadow-sm">
                        <div className="flex space-x-1">
                          {[0, 1, 2].map((i) => (
                            <motion.div
                              key={i}
                              className="w-2 h-2 bg-gray-400 rounded-full"
                              animate={{ y: [0, -8, 0] }}
                              transition={{
                                duration: 0.6,
                                repeat: Infinity,
                                delay: i * 0.15,
                              }}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Suggested Questions */}
                {messages.length === 1 && (
                  <div className="px-4 py-3 bg-white border-t border-gray-100">
                    <div className="text-xs text-gray-500 mb-2">Suggested questions:</div>
                    <div className="flex flex-wrap gap-2">
                      {SUGGESTED_QUESTIONS.map((question, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestedQuestion(question)}
                          className="text-xs px-3 py-1.5 bg-primary-50 text-primary-700 rounded-full hover:bg-primary-100 transition-colors"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Input */}
                <div className="p-4 bg-white border-t border-gray-200">
                  <div className="flex items-end space-x-2">
                    <textarea
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask me anything..."
                      rows={1}
                      className="flex-1 resize-none border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
                    />
                    <button
                      onClick={handleSendMessage}
                      disabled={!input.trim() || isTyping}
                      className="btn-primary p-2.5 disabled:opacity-50"
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-2 text-center">
                    Powered by AI • Always here to help
                  </p>
                </div>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
