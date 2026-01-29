"use client";

import { useEffect, useRef, useState } from "react";
import UnderwaterCard from "./UnderwaterCard";
import BubbleEffect from "./BubbleEffect";

interface JourneyItem {
  image: string;
  title: string;
  description: string;
}

interface UnderwaterJourneyProps {
  items: JourneyItem[];
  onItemClick: (item: JourneyItem) => void;
}

export default function UnderwaterJourney({
  items,
  onItemClick,
}: UnderwaterJourneyProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="journey"
      className="relative py-24 px-6 overflow-hidden"
      style={{
        background:
          "linear-gradient(180deg, #041e2c 0%, #0a4d68 50%, #041e2c 100%)",
      }}
    >
      {/* Background Bubbles */}
      <BubbleEffect count={8} minSize={4} maxSize={16} />

      {/* Light Beams */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="light-beam absolute top-0 left-[20%] w-32 h-full opacity-20"
          style={{ transform: "rotate(15deg)" }}
        />
        <div
          className="light-beam absolute top-0 left-[50%] w-24 h-full opacity-15"
          style={{ transform: "rotate(-5deg)", animationDelay: "1s" }}
        />
        <div
          className="light-beam absolute top-0 right-[25%] w-20 h-full opacity-10"
          style={{ transform: "rotate(10deg)", animationDelay: "2s" }}
        />
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Section Header */}
        <div
          className={`text-center mb-16 transition-all duration-700 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-ocean-300 tracking-[0.3em] text-sm mb-4 font-light uppercase">
            The Story
          </p>
          <h2
            className="text-4xl md:text-5xl font-bold text-white mb-4 text-glow"
            style={{ fontFamily: "'Playfair Display', serif" }}
          >
            Underwater Journey
          </h2>
          <p className="text-aqua/70 max-w-2xl mx-auto">
            From coral reefs to ancient shipwrecks, every dive tells a story
          </p>
        </div>

        {/* Masonry-like Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* First Row - 3 items */}
          {items.slice(0, 3).map((item, index) => (
            <div
              key={index}
              className={`transition-all duration-700 ${
                isVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-12"
              }`}
              style={{ transitionDelay: `${index * 150}ms` }}
            >
              <UnderwaterCard
                image={item.image}
                title={item.title}
                description={item.description}
                index={index}
                onClick={() => onItemClick(item)}
              />
            </div>
          ))}
        </div>

        {/* Second Row - 2 items centered */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6 max-w-4xl mx-auto">
          {items.slice(3, 5).map((item, index) => (
            <div
              key={index + 3}
              className={`transition-all duration-700 ${
                isVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-12"
              }`}
              style={{ transitionDelay: `${(index + 3) * 150}ms` }}
            >
              <UnderwaterCard
                image={item.image}
                title={item.title}
                description={item.description}
                index={index + 3}
                onClick={() => onItemClick(item)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Wave Transition */}
      <div
        className="absolute bottom-0 left-0 right-0 h-24 pointer-events-none"
        style={{
          background: "linear-gradient(to top, #ffffff 0%, transparent 100%)",
        }}
      />
    </section>
  );
}
