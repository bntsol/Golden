"use client";

interface ScrollIndicatorProps {
  targetId?: string;
}

export default function ScrollIndicator({ targetId = "about" }: ScrollIndicatorProps) {
  const handleClick = () => {
    const target = document.getElementById(targetId);
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <button
      onClick={handleClick}
      className="absolute bottom-8 left-1/2 -translate-x-1/2 z-30 flex flex-col items-center gap-2 text-white/80 hover:text-white transition-colors cursor-pointer"
      aria-label="Scroll down"
    >
      <span className="text-sm font-light tracking-wider">Scroll Down</span>
      <div
        className="flex flex-col items-center gap-1"
        style={{ animation: "bounce-soft 2s ease-in-out infinite" }}
      >
        {/* Bubble-style indicator */}
        <div className="w-6 h-10 rounded-full border-2 border-white/50 flex justify-center pt-2">
          <div className="w-1.5 h-3 bg-white/80 rounded-full animate-pulse" />
        </div>
        {/* Arrow */}
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
      </div>
    </button>
  );
}
