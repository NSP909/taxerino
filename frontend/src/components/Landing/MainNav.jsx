import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function MainNav() {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="fixed top-14 left-0 right-0 z-50 p-4"
    >
      <div className="container mx-auto">
        <div className="relative mx-auto max-w-5xl">
          {/* Glassmorphic background */}
          <div className="absolute inset-0 bg-emerald-950/30 backdrop-blur-md rounded-2xl border border-white/10 shadow-lg"></div>

          <div className="relative flex items-center justify-between px-6 py-3">
            {/* Logo */}
            <Link to="/" className="flex items-center group">
              <div className="h-10 w-10 rounded-xl bg-emerald-600/20 border border-emerald-500/20 flex items-center justify-center group-hover:border-emerald-500/40 transition-colors">
                <div className="h-6 w-6 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/50 group-hover:shadow-emerald-500/70"></div>
              </div>
              <span className="ml-3 text-white font-medium tracking-wide">
                Taxerino
              </span>
            </Link>

            {/* Navigation - Centered */}
            <nav className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 hidden md:flex items-center space-x-12">
              <Link
                to="/"
                className="text-white/70 hover:text-white transition-colors text-sm font-medium tracking-wide"
              >
                Home
              </Link>
              <button
                onClick={() =>
                  document
                    .getElementById("features")
                    .scrollIntoView({ behavior: "smooth" })
                }
                className="text-white/70 hover:text-white transition-colors text-sm font-medium tracking-wide"
              >
                Features
              </button>
              <button
                onClick={() =>
                  document
                    .getElementById("contact")
                    .scrollIntoView({ behavior: "smooth" })
                }
                className="text-white/70 hover:text-white transition-colors text-sm font-medium tracking-wide"
              >
                Contact
              </button>
            </nav>

            {/* Right section */}
            <div className="flex items-center">
              <Link
                to="/dashboard"
                className="hidden md:flex px-4 py-2 bg-emerald-600/90 hover:bg-emerald-600 text-white text-sm font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl hover:shadow-emerald-600/20 border border-emerald-500/20"
              >
                Get Started
              </Link>

              {/* Mobile menu button */}
              <button className="md:hidden p-2 hover:bg-white/10 rounded-lg transition-colors">
                <svg
                  className="h-6 w-6 text-white/70"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
}
