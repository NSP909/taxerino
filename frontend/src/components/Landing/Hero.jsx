"use client";

import { Link } from "react-router-dom";
import { ArrowRightIcon } from "@heroicons/react/24/outline";
import starsBg from "../../assets/stars.png";
import {
  motion,
  useMotionValueEvent,
  useScroll,
  useTransform,
} from "framer-motion";
import { useRef } from "react";

export default function Hero() {
  const sectionRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start end", "end start"],
  });

  const backgroundPositionY = useTransform(
    scrollYProgress,
    [0, 1],
    [-300, 300]
  );

  return (
    <motion.section
      ref={sectionRef}
      className="min-h-screen flex items-center overflow-hidden relative pt-32"
      style={{
        backgroundImage: `url(${starsBg})`,
        backgroundPositionY,
      }}
      animate={{
        backgroundPositionX: "100%",
      }}
      transition={{ repeat: Infinity, duration: 60, ease: "linear" }}
    >
      {/* Gradient overlays */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-transparent"></div>
      <div className="absolute inset-0 bg-[radial-gradient(85%_85%_at_center,transparent_0%,rgb(6,78,59)_100%)] opacity-40"></div>
      <div className="absolute inset-0 bg-[radial-gradient(50%_50%_at_center,rgb(16,185,129,0.3)_0%,transparent_80%)]"></div>

      {/* Planet */}
      <div className="absolute h-64 w-64 md:h-96 md:w-96 bg-emerald-500 rounded-full border border-white/20 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[radial-gradient(50%_50%_at_16.8%_18.3%,white,rgb(16,185,129)_37.7%,rgb(6,78,59))] shadow-[-20px_-20px_50px_rgb(255,255,255,.5),-20px_-20px_80px_rgb(255,255,255,.1),0_0_50px_rgb(16,185,129)]"></div>

      {/* Content */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10 text-center w-full max-w-3xl px-4">
        <h1 className="text-8xl md:text-[168px] font-bold tracking-tighter bg-[radial-gradient(100%_100%_at_top_left,white,white,rgb(6,78,59,.5))] text-transparent bg-clip-text leading-none mb-8">
          Taxerino
        </h1>
        <p className="text-lg md:text-xl text-white/70 max-w-2xl mx-auto mb-8">
          Simplify your tax filing journey with AI-powered assistance and secure
          document management.
        </p>
        <Link
          to="/dashboard"
          className="inline-flex items-center px-6 py-3 bg-emerald-600 text-white text-lg font-medium rounded-xl hover:bg-emerald-700 transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          Get Started
          <ArrowRightIcon className="ml-2 h-6 w-6" />
        </Link>
      </div>

      {/* Ring 1 */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
        className="absolute h-[444px] w-[444px] md:h-[680px] md:w-[680px] border opacity-10 rounded-full top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
      >
        <div className="absolute h-2 w-2 left-0 bg-white rounded-full top-1/2 -translate-x-1/2 -translate-y-1/2"></div>
        <div className="absolute h-2 w-2 left-1/2 bg-white rounded-full top-0 -translate-x-1/2 -translate-y-1/2"></div>
        <div className="absolute h-5 w-5 left-full border border-white rounded-full top-1/2 -translate-x-1/2 -translate-y-1/2 inline-flex items-center justify-center">
          <div className="h-2 w-2 bg-white rounded-full"></div>
        </div>
      </motion.div>

      {/* Ring 2 */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 45, repeat: Infinity, ease: "linear" }}
        className="absolute h-[544px] w-[544px] md:h-[880px] md:w-[880px] rounded-full border border-white/10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border-dashed"
      ></motion.div>

      {/* Ring 3 */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
        className="absolute h-[644px] w-[644px] md:h-[1080px] md:w-[1080px] rounded-full border border-white opacity-10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
      >
        <div className="absolute h-2 w-2 left-0 bg-white rounded-full top-1/2 -translate-x-1/2 -translate-y-1/2"></div>
        <div className="absolute h-2 w-2 left-full bg-white rounded-full top-1/2 -translate-x-1/2 -translate-y-1/2"></div>
      </motion.div>
    </motion.section>
  );
}
