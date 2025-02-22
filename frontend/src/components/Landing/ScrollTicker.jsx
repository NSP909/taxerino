"use client";
import { motion } from "framer-motion";
import bgbLogo from "../../assets/bgb.png";
import caponeLogo from "../../assets/capone.png";
import coinbaseLogo from "../../assets/coinbase.png";
import devpostLogo from "../../assets/devpost.png";
import dshawLogo from "../../assets/dshaw.png";
import eqvLogo from "../../assets/eqv.png";

export const ScrollTicker = () => {
  const logos = [
    bgbLogo,
    caponeLogo,
    coinbaseLogo,
    devpostLogo,
    dshawLogo,
    eqvLogo,
    // Repeat for continuous scroll
    bgbLogo,
    caponeLogo,
    coinbaseLogo,
    devpostLogo,
    dshawLogo,
    eqvLogo,
  ];

  return (
    <section className="py-16 bg-transparent absolute bottom-0 left-0 right-0 z-10">
      <div className="absolute inset-0 bg-emerald-950/60 backdrop-blur-sm"></div>
      <div className="max-w-7xl mx-auto px-4 relative z-20">
        <div className="flex flex-col md:flex-row items-center justify-center gap-8">
          <h2 className="text-emerald-100/70 text-sm md:text-base font-medium text-center md:text-left whitespace-nowrap">
            Trusted by leading companies
          </h2>
          <div className="flex-1 overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_20%,black_80%,transparent)]">
            <motion.div
              animate={{
                x: ["-25%", "-50%"],
              }}
              transition={{
                duration: 20,
                repeat: Infinity,
                ease: "linear",
              }}
              className="flex items-center justify-center gap-20"
            >
              {logos.map((logo, index) => (
                <img
                  key={index}
                  src={logo}
                  alt="Company logo"
                  className="h-10 w-auto object-contain opacity-70 hover:opacity-100 transition-opacity"
                />
              ))}
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
};
