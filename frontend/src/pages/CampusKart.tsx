import { useState, useEffect } from 'react';
import { 
  FaGraduationCap, 
  FaShoppingBag, 
  FaPalette, 
  FaBook, 
  FaArrowRight, 
  FaInstagram, 
  FaTwitter, 
  FaTiktok,
  FaEnvelope,
  FaCheck,
  FaClock,
  FaUsers,
  FaHandshake
} from 'react-icons/fa';

const CampusKart = () => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [timeLeft, setTimeLeft] = useState({
    days: 30,
    hours: 12,
    minutes: 45,
    seconds: 30
  });

  // Countdown timer effect
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: prev.minutes - 1, seconds: 59 };
        } else if (prev.hours > 0) {
          return { ...prev, hours: prev.hours - 1, minutes: 59, seconds: 59 };
        } else if (prev.days > 0) {
          return { ...prev, days: prev.days - 1, hours: 23, minutes: 59, seconds: 59 };
        }
        return prev;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    if (!email) return;
    
    // Simulate successful submission
    setIsSubmitted(true);
    
    // Reset after 4 seconds
    setTimeout(() => {
      setIsSubmitted(false);
      setEmail('');
    }, 4000);
  };

  const features = [
    {
      icon: <FaShoppingBag className="w-8 h-8" />,
      title: "Sell Handmade Goods",
      description: "From custom tote bags to artisanal soaps - showcase your creativity",
      color: "text-purple-500"
    },
    {
      icon: <FaPalette className="w-8 h-8" />,
      title: "Offer Services",
      description: "Hair styling, graphic design, tutoring - monetize your skills",
      color: "text-teal-500"
    },
    {
      icon: <FaBook className="w-8 h-8" />,
      title: "Second-hand Items",
      description: "Perfect for final year students - sell what you no longer need",
      color: "text-indigo-500"
    }
  ];

  const stats = [
    { number: "500+", label: "Students Interested", icon: <FaUsers /> },
    { number: "15+", label: "Universities", icon: <FaGraduationCap /> },
    { number: "100+", label: "Pre-orders", icon: <FaHandshake /> }
  ];

  const faqs = [
    {
      question: "What is CampusKart?",
      answer: "CampusKart is a marketplace designed specifically for university students to buy and sell goods and services within their campus community."
    },
    {
      question: "Who can use CampusKart?",
      answer: "Any enrolled university or college student can join our platform to start their entrepreneurial journey."
    },
    {
      question: "When will it launch?",
      answer: "We're launching very soon! Sign up to be the first to know when we go live."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-teal-50 dark:from-gray-900 dark:via-purple-900 dark:to-teal-900">
      {/* Header */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-teal-600/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-teal-600 rounded-2xl flex items-center justify-center shadow-lg">
                <FaGraduationCap className="text-white text-xl" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-teal-600 bg-clip-text text-transparent">
                  CampusKart
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">Student Marketplace</p>
              </div>
            </div>
            <div className="bg-gradient-to-r from-purple-100 to-teal-100 dark:from-purple-800 dark:to-teal-800 px-4 py-2 rounded-full">
              <span className="text-sm font-medium text-purple-800 dark:text-purple-200">Coming Soon</span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
          <div className="text-center space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500/20 to-teal-500/20 border border-purple-500/30 rounded-full px-6 py-3 animate-pulse">
              <FaClock className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Launching Soon for Campus Entrepreneurs
              </span>
            </div>

            {/* Main Headline */}
            <div className="space-y-6">
              <h2 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-800 dark:text-white leading-tight">
                Buy. Sell. Hustle Smart
                <span className="bg-gradient-to-r from-purple-600 via-indigo-600 to-teal-600 bg-clip-text text-transparent block">
                  Right from Campus
                </span>
              </h2>
              <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed">
                The first student-exclusive marketplace where university entrepreneurs turn dorms into storefronts. 
                Sell handmade goods, offer services, or find great deals on campus.
              </p>
            </div>

            {/* Countdown Timer */}
            <div className="max-w-2xl mx-auto">
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-6">Launch Countdown</h3>
              <div className="grid grid-cols-4 gap-4 mb-8">
                {[
                  { value: timeLeft.days, label: 'Days' },
                  { value: timeLeft.hours, label: 'Hours' },
                  { value: timeLeft.minutes, label: 'Minutes' },
                  { value: timeLeft.seconds, label: 'Seconds' }
                ].map((item, index) => (
                  <div key={index} className="bg-white dark:bg-gray-800 rounded-2xl p-4 shadow-lg border border-purple-100 dark:border-purple-800">
                    <div className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-purple-600 to-teal-600 bg-clip-text text-transparent">
                      {item.value.toString().padStart(2, '0')}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {item.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-8 mt-16 max-w-6xl mx-auto">
              {features.map((feature, index) => (
                <div key={index} className="bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 dark:border-gray-700">
                  <div className="flex flex-col items-center text-center space-y-4">
                    <div className={`p-4 bg-gradient-to-r from-purple-100 to-teal-100 dark:from-purple-800 dark:to-teal-800 rounded-2xl ${feature.color}`}>
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-white">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 mt-16 max-w-3xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-purple-600 dark:text-purple-400 text-2xl mb-2 flex justify-center">
                    {stat.icon}
                  </div>
                  <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-purple-600 to-teal-600 bg-clip-text text-transparent">
                    {stat.number}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>

            {/* Email Signup */}
            <div className="max-w-2xl mx-auto mt-16">
              {!isSubmitted ? (
                <div className="bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-2xl border border-purple-100 dark:border-purple-800">
                  <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
                    Be the First to Know! 🎓
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    Join thousands of students waiting to start their campus hustle
                  </p>
                  <form onSubmit={handleEmailSubmit} className="space-y-4">
                    <div className="flex items-center bg-gray-50 dark:bg-gray-700 rounded-2xl p-4 focus-within:ring-2 focus-within:ring-purple-500">
                      <FaEnvelope className="w-5 h-5 text-gray-400 mr-3" />
                      <input
                        type="email"
                        placeholder="Enter your university email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="flex-1 bg-transparent outline-none text-gray-800 dark:text-white placeholder-gray-500"
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      className="w-full group relative overflow-hidden bg-gradient-to-r from-purple-600 to-teal-600 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 hover:scale-105 hover:shadow-lg"
                    >
                      <div className="flex items-center justify-center space-x-2">
                        <span>Notify Me When We Launch</span>
                        <FaArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                      </div>
                      <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                    </button>
                  </form>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-4 text-center">
                    We respect your privacy. No spam, only launch updates.
                  </p>
                </div>
              ) : (
                <div className="bg-gradient-to-r from-green-50 to-teal-50 dark:from-green-900 dark:to-teal-900 border border-green-200 dark:border-green-700 rounded-3xl p-8 text-center">
                  <div className="w-16 h-16 bg-green-100 dark:bg-green-800 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FaCheck className="w-8 h-8 text-green-600 dark:text-green-400 animate-bounce" />
                  </div>
                  <h3 className="text-2xl font-bold text-green-800 dark:text-green-400 mb-2">You're In! 🎉</h3>
                  <p className="text-green-700 dark:text-green-300">
                    Thanks for joining the CampusKart community! We'll notify you as soon as we launch.
                  </p>
                </div>
              )}
            </div>

            {/* Mission Statement */}
            <div className="mt-16 bg-gradient-to-r from-purple-500/5 to-teal-500/5 dark:from-purple-500/10 dark:to-teal-500/10 rounded-3xl p-8 border border-purple-200/30 dark:border-purple-700/30 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Our Mission</h3>
              <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                We believe every student has entrepreneurial potential. CampusKart provides a safe, 
                trusted platform where students can turn their skills, creativity, and unused items 
                into income while building valuable business experience.
              </p>
            </div>

            {/* FAQ */}
            <div className="mt-16 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-8 text-center">Frequently Asked Questions</h3>
              <div className="grid gap-6">
                {faqs.map((faq, index) => (
                  <div key={index} className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-100 dark:border-gray-700">
                    <h4 className="font-semibold text-gray-800 dark:text-white mb-2">{faq.question}</h4>
                    <p className="text-gray-600 dark:text-gray-300">{faq.answer}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-purple-900 to-teal-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center space-y-8">
            {/* Logo */}
            <div className="flex justify-center items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-400 to-teal-400 rounded-xl flex items-center justify-center">
                <FaGraduationCap className="text-white text-lg" />
              </div>
              <span className="text-2xl font-bold">CampusKart</span>
            </div>

            {/* Social Links */}
            <div className="flex justify-center space-x-6">
              <a href="#" className="text-gray-300 hover:text-purple-400 transition-colors p-3 bg-white/10 rounded-full hover:bg-white/20">
                <FaInstagram className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-300 hover:text-purple-400 transition-colors p-3 bg-white/10 rounded-full hover:bg-white/20">
                <FaTwitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-300 hover:text-purple-400 transition-colors p-3 bg-white/10 rounded-full hover:bg-white/20">
                <FaTiktok className="w-5 h-5" />
              </a>
              <a href="mailto:hello@campuskart.com" className="text-gray-300 hover:text-purple-400 transition-colors p-3 bg-white/10 rounded-full hover:bg-white/20">
                <FaEnvelope className="w-5 h-5" />
              </a>
            </div>

            {/* Contact Info */}
            <div className="text-center space-y-2">
              <p className="text-gray-300">
                Questions? Reach out at{' '}
                <a href="mailto:hello@campuskart.com" className="text-purple-400 hover:underline">
                  hello@campuskart.com
                </a>
              </p>
            </div>

            {/* Copyright */}
            <div className="border-t border-gray-700 pt-8">
              <p className="text-gray-400 text-sm">
                © 2025 CampusKart. All rights reserved. Empowering Campus Entrepreneurs.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CampusKart;