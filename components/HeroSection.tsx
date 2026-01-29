"use client";

import Image from "next/image";
import BubbleEffect from "./BubbleEffect";
import ScrollIndicator from "./ScrollIndicator";

interface HeroSectionProps {
  name: string;
  tagline: string;
  backgroundImage: string;
}

export default function HeroSection({
  name,
  tagline,
  backgroundImage,
}: HeroSectionProps) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image - Optimized with Next.js Image */}
      <Image
        src={backgroundImage}
        alt="Underwater Adventure Background"
        fill
        priority
        quality={85}
        className="object-cover"
        sizes="100vw"
      />

      {/* Gradient Overlay - Deep ocean feel */}
      <div
        className="absolute inset-0 z-10"
        style={{
          background:
            "linear-gradient(180deg, rgba(5, 25, 35, 0.4) 0%, rgba(10, 77, 104, 0.3) 40%, rgba(5, 25, 35, 0.6) 100%)",
        }}
      />

      {/* Light Beams from surface */}
      <div className="absolute inset-0 z-10 pointer-events-none overflow-hidden">
        <div
          className="light-beam absolute -top-20 left-[15%] w-40 h-[120%] opacity-30"
          style={{ transform: "rotate(10deg)" }}
        />
        <div
          className="light-beam absolute -top-20 left-[35%] w-24 h-[120%] opacity-20"
          style={{ transform: "rotate(-5deg)", animationDelay: "1.5s" }}
        />
        <div
          className="light-beam absolute -top-20 right-[30%] w-32 h-[120%] opacity-25"
          style={{ transform: "rotate(8deg)", animationDelay: "0.8s" }}
        />
        <div
          className="light-beam absolute -top-20 right-[15%] w-20 h-[120%] opacity-15"
          style={{ transform: "rotate(-12deg)", animationDelay: "2s" }}
        />
      </div>

      {/* Bubble Effect */}
      <BubbleEffect
        count={15}
        minSize={6}
        maxSize={24}
        minDuration={8}
        maxDuration={16}
      />

      {/* Top Wave Effect */}
      <div className="absolute top-0 left-0 right-0 h-32 z-20 pointer-events-none overflow-hidden">
        <svg
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
          className="absolute w-[200%] h-full rotate-180"
          style={{ animation: "wave 6s ease-in-out infinite" }}
        >
          <path
            d="M0,60 C150,20 350,100 600,60 C850,20 1050,100 1200,60 L1200,0 L0,0 Z"
            fill="rgba(184, 224, 255, 0.1)"
          />
        </svg>
      </div>

      {/* Content */}
      <div className="relative z-30 text-center text-white px-6 max-w-4xl mx-auto">
        <p className="text-ocean-200 tracking-[0.4em] text-sm mb-6 font-light uppercase animate-pulse">
          Welcome to the Deep
        </p>
        <h1
          className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 text-glow"
          style={{
            fontFamily: "'Playfair Display', serif",
            animation: "fade-in-up 1s ease-out",
          }}
        >
          {name}
        </h1>
        <p
          className="text-xl md:text-2xl text-aqua/90 max-w-2xl mx-auto font-light leading-relaxed"
          style={{ animation: "fade-in-up 1s ease-out 0.3s both" }}
        >
          {tagline}
        </p>

        {/* Decorative Elements */}
        <div
          className="mt-8 flex justify-center gap-4"
          style={{ animation: "fade-in-up 1s ease-out 0.6s both" }}
        >
          <div className="w-16 h-[1px] bg-gradient-to-r from-transparent via-ocean-300 to-transparent" />
          <div className="w-2 h-2 rounded-full bg-ocean-300 animate-pulse" />
          <div className="w-16 h-[1px] bg-gradient-to-r from-transparent via-ocean-300 to-transparent" />
        </div>
      </div>

      {/* Scroll Indicator */}
      <ScrollIndicator targetId="about" />

      {/* Bottom Gradient for smooth transition */}
      <div
        className="absolute bottom-0 left-0 right-0 h-40 z-20 pointer-events-none"
        style={{
          background:
            "linear-gradient(to top, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.5) 50%, transparent 100%)",
        }}
      />
    </section>
  );
}
