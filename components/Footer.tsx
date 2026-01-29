"use client";

import BubbleEffect from "./BubbleEffect";

interface FooterProps {
  name: string;
}

export default function Footer({ name }: FooterProps) {
  return (
    <footer className="relative py-16 px-6 overflow-hidden bg-deep-sea">
      {/* Background Bubbles */}
      <BubbleEffect count={6} minSize={3} maxSize={12} minDuration={10} maxDuration={18} />

      {/* Light beams */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="light-beam absolute -top-20 left-[30%] w-16 h-[150%] opacity-10"
          style={{ transform: "rotate(5deg)" }}
        />
        <div
          className="light-beam absolute -top-20 right-[40%] w-12 h-[150%] opacity-5"
          style={{ transform: "rotate(-8deg)", animationDelay: "2s" }}
        />
      </div>

      <div className="max-w-5xl mx-auto text-center relative z-10">
        <h3
          className="text-3xl font-semibold mb-4 text-white text-glow"
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          {name}
        </h3>

        {/* Decorative wave */}
        <div className="mt-8 mb-8">
          <svg
            className="mx-auto opacity-30"
            width="200"
            height="20"
            viewBox="0 0 200 20"
          >
            <path
              d="M0,10 C25,0 50,20 75,10 C100,0 125,20 150,10 C175,0 200,20 200,10"
              stroke="#088395"
              strokeWidth="2"
              fill="none"
            />
          </svg>
        </div>

        <div className="pt-4 border-t border-ocean-800/50">
          <p className="text-ocean-500 text-sm">
            Built with Next.js & Tailwind CSS
          </p>
          <p className="text-ocean-600 text-xs mt-2">
            Diving into code, one line at a time
          </p>
        </div>
      </div>
    </footer>
  );
}
