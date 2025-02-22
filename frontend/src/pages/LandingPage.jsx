import { useRef } from "react";
import Hero from "../components/Landing/Hero";
import { ScrollTicker } from "../components/Landing/ScrollTicker";
import MainNav from "../components/Landing/MainNav";
import {
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";
import { motion } from "framer-motion";

const features = [
  {
    icon: DocumentTextIcon,
    title: "Easy Document Management",
    description:
      "Upload and organize your tax documents securely. Support for various formats and automatic categorization.",
  },
  {
    icon: ChatBubbleLeftRightIcon,
    title: "AI Tax Assistant",
    description:
      "Get instant answers to your tax questions from our intelligent assistant, available 24/7.",
  },
  {
    icon: ShieldCheckIcon,
    title: "Bank-Level Security",
    description:
      "Your data is protected with enterprise-grade encryption and security measures.",
  },
];

const benefits = [
  "Automated document processing",
  "Real-time tax calculations",
  "Expert AI assistance",
  "Secure data storage",
  "Easy file organization",
  "24/7 availability",
];

export default function LandingPage() {
  const featuresRef = useRef(null);
  const contactRef = useRef(null);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-emerald-950">
      <MainNav
        scrollToHome={scrollToTop}
        scrollToFeatures={() => scrollToSection(featuresRef)}
        scrollToContact={() => scrollToSection(contactRef)}
      />
      <Hero />
      <ScrollTicker />

      {/* Features Section */}
      <motion.section
        ref={featuresRef}
        id="features"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="py-24 bg-emerald-900"
      >
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-white mb-12">
            Everything you need to manage your taxes
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="bg-emerald-800/50 backdrop-blur-sm rounded-2xl p-8 border border-emerald-700/30"
              >
                <div className="h-12 w-12 bg-emerald-700 rounded-xl flex items-center justify-center mb-6">
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-emerald-100/70">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Benefits Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="py-24 bg-gradient-to-b from-emerald-900 to-emerald-950"
      >
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Why choose Taxerino?
            </h2>
            <p className="text-lg text-emerald-100/70 mb-12">
              Experience a smarter way to handle your taxes with our
              comprehensive suite of features.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {benefits.map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="flex items-center space-x-3 bg-emerald-800/30 rounded-xl p-4"
              >
                <CheckCircleIcon className="h-6 w-6 text-emerald-400" />
                <span className="text-white">{benefit}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Contact Section */}
      <motion.section
        ref={contactRef}
        id="contact"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="py-24 bg-emerald-950"
      >
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to simplify your taxes?
          </h2>
          <p className="text-lg text-emerald-100/70 mb-8 max-w-2xl mx-auto">
            Join thousands of users who have made tax filing easier with
            Taxerino. Start your journey today.
          </p>
          <a
            href="/dashboard"
            className="inline-flex items-center px-8 py-4 bg-emerald-600 text-white text-lg font-medium rounded-xl hover:bg-emerald-700 transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            Get Started Now
          </a>
        </div>
      </motion.section>
    </div>
  );
}
