import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  Users,
  MessageSquare,
  TrendingUp,
  Zap,
  Shield,
  ArrowRight,
  CheckCircle2,
  Brain,
  Network,
  Target,
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-lg border-b border-gray-200 z-50">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gradient">Bond.AI</span>
            </Link>

            <div className="flex items-center space-x-4">
              <Link to="/login" className="btn-ghost">
                Login
              </Link>
              <Link to="/signup" className="btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 overflow-hidden">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="inline-flex items-center space-x-2 px-4 py-2 bg-primary-50 rounded-full mb-6">
                <Sparkles className="w-4 h-4 text-primary-600" />
                <span className="text-sm font-medium text-primary-700">
                  AI-Powered Connection Intelligence
                </span>
              </div>

              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                Build{' '}
                <span className="text-gradient">Meaningful</span>
                <br />
                Partnerships with AI
              </h1>

              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Bond.AI uses intelligent agents to understand what you need and what you offer,
                then finds perfect matches through AI-powered conversations. No more awkward networking.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/signup" className="btn-primary text-lg px-8 py-4">
                  Start Matching
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
                <button className="btn-outline text-lg px-8 py-4">
                  Watch Demo
                </button>
              </div>

              <div className="mt-12 flex items-center space-x-8">
                <div>
                  <div className="text-3xl font-bold text-gray-900">10K+</div>
                  <div className="text-sm text-gray-600">Active Users</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">85%</div>
                  <div className="text-sm text-gray-600">Match Success</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">50K+</div>
                  <div className="text-sm text-gray-600">Connections Made</div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-2xl bg-gradient-to-br from-primary-50 to-secondary-50 p-8 shadow-2xl">
                <div className="space-y-4">
                  {/* Mock chat messages */}
                  <div className="bg-white rounded-xl p-4 shadow-sm">
                    <div className="flex items-start space-x-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center">
                        <Brain className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900">Your AI Agent</div>
                        <div className="text-sm text-gray-600 mt-1">
                          I found 3 perfect matches for your startup funding needs!
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white rounded-xl p-4 shadow-sm ml-8">
                    <div className="flex items-start space-x-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-secondary flex items-center justify-center">
                        <Users className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900">Partner Agent</div>
                        <div className="text-sm text-gray-600 mt-1">
                          My client offers seed funding and is interested in AI startups.
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-primary-600 text-white rounded-xl p-4 shadow-sm">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CheckCircle2 className="w-5 h-5" />
                        <span className="font-medium">Match confirmed!</span>
                      </div>
                      <span className="text-sm opacity-90">95% fit</span>
                    </div>
                  </div>
                </div>

                {/* Floating elements */}
                <motion.div
                  className="absolute -top-4 -right-4 bg-white rounded-xl p-4 shadow-lg"
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 3, repeat: Infinity }}
                >
                  <div className="flex items-center space-x-2">
                    <Zap className="w-5 h-5 text-yellow-500" />
                    <span className="text-sm font-medium">AI Negotiating...</span>
                  </div>
                </motion.div>

                <motion.div
                  className="absolute -bottom-4 -left-4 bg-white rounded-xl p-4 shadow-lg"
                  animate={{ y: [0, 10, 0] }}
                  transition={{ duration: 3, repeat: Infinity, delay: 1 }}
                >
                  <div className="flex items-center space-x-2">
                    <Network className="w-5 h-5 text-green-500" />
                    <span className="text-sm font-medium">3 New Matches</span>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gray-50">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How Bond.AI Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our AI agents work behind the scenes to find perfect matches and negotiate terms
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Target,
                title: 'Define Your Needs',
                description: 'Tell us what you need and what you can offer. Our AI understands context and nuance.',
                color: 'from-blue-500 to-cyan-500',
              },
              {
                icon: Brain,
                title: 'AI Agents Match',
                description: 'Your personal AI agent negotiates with other agents to find the perfect partnerships.',
                color: 'from-purple-500 to-pink-500',
              },
              {
                icon: MessageSquare,
                title: 'Connect & Collaborate',
                description: 'Review AI-negotiated terms and connect with verified, high-quality matches.',
                color: 'from-orange-500 to-red-500',
              },
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card relative overflow-hidden group hover:shadow-xl transition-shadow"
              >
                <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${step.color}`} />
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${step.color} flex items-center justify-center mb-4`}>
                  <step.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {index + 1}. {step.title}
                </h3>
                <p className="text-gray-600">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Features that make Bond.AI the smartest way to build professional relationships
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: 'Semantic Matching',
                description: 'NLP-powered matching understands context and meaning, not just keywords.',
              },
              {
                icon: MessageSquare,
                title: 'Agent Negotiation',
                description: 'AI agents negotiate terms on your behalf, finding win-win outcomes.',
              },
              {
                icon: TrendingUp,
                title: 'Learning Algorithms',
                description: 'Reinforcement learning improves match quality over time.',
              },
              {
                icon: Zap,
                title: 'Real-Time Notifications',
                description: 'Get instant updates on matches, proposals, and agreements.',
              },
              {
                icon: Shield,
                title: 'Privacy First',
                description: 'Your data stays private. Local LLM processing, no data selling.',
              },
              {
                icon: Network,
                title: 'LinkedIn Integration',
                description: 'Import your network and leverage existing connections.',
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                viewport={{ once: true }}
                className="card hover:border-primary-200 transition-colors"
              >
                <feature.icon className="w-10 h-10 text-primary-600 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-accent">
        <div className="container-custom text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Build Smarter Connections?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of professionals using AI to find perfect partnerships
            </p>
            <Link to="/signup" className="btn bg-white text-primary-600 hover:bg-gray-100 text-lg px-8 py-4">
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gray-900">
        <div className="container-custom">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 rounded-lg bg-gradient-accent flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Bond.AI</span>
            </div>

            <div className="flex space-x-8 text-gray-400 text-sm">
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
              <a href="#" className="hover:text-white transition-colors">Terms</a>
              <a href="#" className="hover:text-white transition-colors">Contact</a>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400 text-sm">
            © 2025 Bond.AI. Built with AI for better connections.
          </div>
        </div>
      </footer>
    </div>
  );
}
