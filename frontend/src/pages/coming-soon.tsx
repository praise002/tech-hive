import React, { useState } from 'react';
import { FaLinkedin, FaTwitter, FaInstagram, FaArrowRight, FaStar, FaUsers, FaTrophy, FaRocket } from 'react-icons/fa';
import { HiMail } from 'react-icons/hi';


const ComingSoon: React.FC = () => {
  const [email, setEmail] = useState('');
  const [creatorType, setCreatorType] = useState<'small' | 'big' | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleEmailSubmit = (e: React.FormEvent, type: 'small' | 'big') => {
    e.preventDefault();
    if (!email) return;
    
    setCreatorType(type);
    // Here you would integrate with your form service
    // For now, we'll simulate a successful submission
    setIsSubmitted(true);
    
    // Reset after 3 seconds
    setTimeout(() => {
      setIsSubmitted(false);
      setEmail('');
      setCreatorType(null);
    }, 3000);
  };

  const features = [
    {
      icon: <FaStar className="w-8 h-8 text-orange" />,
      title: "Monetize Content",
      description: "Turn your LinkedIn posts into revenue streams"
    },
    {
      icon: <FaUsers className="w-8 h-8 text-primary-light" />,
      title: "Link Monetization", 
      description: "Earn from every click with smart link tracking"
    },
    {
      icon: <FaTrophy className="w-8 h-8 text-lime-green" />,
      title: "Digital Products",
      description: "Sell courses, ebooks, and services seamlessly"
    }
  ];

  const stats = [
    { number: "10K+", label: "Creators Waiting" },
    { number: "500K+", label: "Expected Revenue" },
    { number: "25+", label: "Countries" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-custom-white via-neutral to-light dark:from-dark dark:via-primary dark:to-gray-900">
      {/* Header */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-light/10 to-orange/10 dark:from-primary-light/5 dark:to-orange/5"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-light to-orange rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">C</span>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-light to-orange bg-clip-text text-transparent">
                Credlink
              </h1>
            </div>
            <div className="text-sm text-secondary dark:text-gray-400">
              Coming Soon
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
          <div className="text-center space-y-8">
            {/* Animated Badge */}
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-primary-light/20 to-orange/20 border border-primary-light/30 rounded-full px-4 py-2 animate-pulse">
              <FaRocket className="w-4 h-4 text-primary-light" />
              <span className="text-sm font-medium text-primary dark:text-custom-white">
                Launching Soon for LinkedIn Creators
              </span>
            </div>

            {/* Main Headline */}
            <div className="space-y-4">
              <h2 className="text-4xl md:text-6xl lg:text-7xl font-bold text-primary dark:text-custom-white leading-tight">
                Monetize Your 
                <span className="bg-gradient-to-r from-primary-light to-orange bg-clip-text text-transparent block">
                  LinkedIn Influence
                </span>
              </h2>
              <p className="text-xl md:text-2xl text-secondary dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
                The first platform designed specifically for LinkedIn creators to turn their content, 
                links, and expertise into sustainable revenue streams.
              </p>
            </div>

            {/* Problem & Solution */}
            <div className="max-w-4xl mx-auto">
              <div className="grid md:grid-cols-2 gap-8 mt-12">
                <div className="bg-red/5 dark:bg-red/10 rounded-2xl p-6 border border-red/20">
                  <h3 className="text-lg font-semibold text-red mb-3">The Problem</h3>
                  <p className="text-gray-700 dark:text-gray-300">
                    LinkedIn creators struggle to monetize their growing influence. 
                    Existing platforms don't understand the professional nature of LinkedIn content.
                  </p>
                </div>
                <div className="bg-lime-green/5 dark:bg-lime-green/10 rounded-2xl p-6 border border-lime-green/20">
                  <h3 className="text-lg font-semibold text-lime-green mb-3">Our Solution</h3>
                  <p className="text-gray-700 dark:text-gray-300">
                    Credlink bridges this gap with tools designed for professional creators, 
                    from content monetization to smart link tracking and product sales.
                  </p>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-8 mt-16">
              {features.map((feature, index) => (
                <div key={index} className="bg-white dark:bg-primary/50 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <div className="flex flex-col items-center text-center space-y-4">
                    <div className="p-3 bg-gradient-to-r from-primary-light/10 to-orange/10 rounded-full">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-semibold text-primary dark:text-custom-white">
                      {feature.title}
                    </h3>
                    <p className="text-secondary dark:text-gray-300">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary-light to-orange bg-clip-text text-transparent">
                    {stat.number}
                  </div>
                  <div className="text-sm text-secondary dark:text-gray-400 mt-1">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>

            {/* Waitlist Form */}
            <div className="max-w-2xl mx-auto mt-16">
              {!isSubmitted ? (
                <div className="bg-white dark:bg-primary/30 rounded-3xl p-8 shadow-2xl border border-gray-200 dark:border-gray-700">
                  <h3 className="text-2xl font-bold text-primary dark:text-custom-white mb-6">
                    Join the Waitlist
                  </h3>
                  <form className="space-y-6">
                    <div className="flex items-center bg-neutral dark:bg-gray-800 rounded-xl p-4 focus-within:ring-2 focus-within:ring-primary-light">
                      <HiMail className="w-5 h-5 text-secondary dark:text-gray-400 mr-3" />
                      <input
                        type="email"
                        placeholder="Enter your email address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="flex-1 bg-transparent outline-none text-primary dark:text-custom-white placeholder-secondary dark:placeholder-gray-400"
                        required
                      />
                    </div>
                    <div className="grid md:grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={(e) => handleEmailSubmit(e, 'small')}
                        className="group relative overflow-hidden bg-gradient-to-r from-primary-light to-orange text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-lg"
                      >
                        <div className="flex items-center justify-center space-x-2">
                          <FaUsers className="w-4 h-4" />
                          <span>I'm a Small Creator</span>
                          <FaArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </div>
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                      </button>
                      <button
                        type="button"
                        onClick={(e) => handleEmailSubmit(e, 'big')}
                        className="group relative overflow-hidden bg-gradient-to-r from-orange to-honey text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-lg"
                      >
                        <div className="flex items-center justify-center space-x-2">
                          <FaTrophy className="w-4 h-4" />
                          <span>I'm a Big Creator</span>
                          <FaArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </div>
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                      </button>
                    </div>
                  </form>
                  <p className="text-xs text-secondary dark:text-gray-400 mt-4 text-center">
                    No spam. We'll only send you updates about Credlink's launch.
                  </p>
                </div>
              ) : (
                <div className="bg-lime-green/10 dark:bg-lime-green/20 border border-lime-green/30 rounded-3xl p-8 text-center">
                  <div className="w-16 h-16 bg-lime-green/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FaArrowRight className="w-8 h-8 text-lime-green animate-bounce" />
                  </div>
                  <h3 className="text-2xl font-bold text-lime-green mb-2">Welcome aboard!</h3>
                  <p className="text-secondary dark:text-gray-300">
                    Thanks for joining our waitlist as a <span className="font-semibold">{creatorType} creator</span>. 
                    We'll be in touch soon with exclusive early access.
                  </p>
                </div>
              )}
            </div>

            {/* Testimonial Space */}
            <div className="mt-16 bg-gradient-to-r from-primary-light/5 to-orange/5 dark:from-primary-light/10 dark:to-orange/10 rounded-3xl p-8 border border-primary-light/20">
              <div className="text-center space-y-4">
                <div className="flex justify-center space-x-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <FaStar key={i} className="w-5 h-5 text-orange" />
                  ))}
                </div>
                <p className="text-lg italic text-primary dark:text-custom-white">
                  "Finally, a platform that understands LinkedIn creators! Can't wait to start monetizing my content the right way."
                </p>
                <div className="font-semibold text-secondary dark:text-gray-300">
                  - Early Beta Tester
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-primary dark:bg-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center space-y-8">
            {/* Logo */}
            <div className="flex justify-center items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-light to-orange rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">C</span>
              </div>
              <span className="text-xl font-bold">Credlink</span>
            </div>

            {/* Social Links */}
            <div className="flex justify-center space-x-6">
              <a href="#" className="text-gray-400 hover:text-primary-light transition-colors p-2">
                <FaLinkedin className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-light transition-colors p-2">
                <FaTwitter className="w-6 h-6" />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-light transition-colors p-2">
                <FaInstagram className="w-6 h-6" />
              </a>
              <a href="mailto:hello@credlink.com" className="text-gray-400 hover:text-primary-light transition-colors p-2">
                <HiMail className="w-6 h-6" />
              </a>
            </div>

            {/* Contact Info */}
            <div className="text-center space-y-2">
              <p className="text-gray-400">
                Questions? Reach us at{' '}
                <a href="mailto:hello@credlink.com" className="text-primary-light hover:underline">
                  hello@credlink.com
                </a>
              </p>
            </div>

            {/* Copyright */}
            <div className="border-t border-gray-700 pt-8">
              <p className="text-gray-400 text-sm">
                © 2025 Credlink. All rights reserved. Built for LinkedIn creators, by creators.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ComingSoon;