"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";

interface AboutSectionProps {
  profileImage: string;
  greeting: string;
  description: string;
  highlights: string[];
}

export default function AboutSection({
  profileImage,
  greeting,
  description,
  highlights,
}: AboutSectionProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [isImageHovered, setIsImageHovered] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.2 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="about"
      className="py-24 px-6 relative overflow-hidden"
      style={{
        background:
          "linear-gradient(180deg, #ffffff 0%, #e6f4f9 50%, #b8e0ff 100%)",
      }}
    >
      {/* Subtle wave pattern background */}
      <div className="absolute inset-0 opacity-30 pointer-events-none">
        <svg
          className="absolute bottom-0 left-0 w-full"
          viewBox="0 0 1200 200"
          preserveAspectRatio="none"
        >
          <path
            d="M0,100 C200,150 400,50 600,100 C800,150 1000,50 1200,100 L1200,200 L0,200 Z"
            fill="rgba(8, 131, 149, 0.1)"
          />
        </svg>
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        <h2
          className={`text-3xl md:text-4xl font-semibold text-center mb-16 text-ocean-600 transition-all duration-700 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          About Me
        </h2>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Profile Image - Circular frame with fish school effect */}
          <div
            className={`relative transition-all duration-700 delay-150 ${
              isVisible
                ? "opacity-100 translate-x-0"
                : "opacity-0 -translate-x-12"
            }`}
          >
            <div
              className="relative mx-auto"
              style={{ maxWidth: "400px" }}
              onMouseEnter={() => setIsImageHovered(true)}
              onMouseLeave={() => setIsImageHovered(false)}
            >
              {/* Circular Image Container */}
              <div
                className={`aspect-square rounded-full overflow-hidden shadow-2xl relative transition-transform duration-500 ${
                  isImageHovered ? "scale-105" : "scale-100"
                }`}
                style={{
                  boxShadow: isImageHovered
                    ? "0 0 60px rgba(8, 131, 149, 0.5)"
                    : "0 25px 50px rgba(0, 0, 0, 0.15)",
                }}
              >
                <Image
                  src={profileImage}
                  alt="Profile"
                  fill
                  quality={85}
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 400px"
                />

                {/* Hover overlay with bubbles */}
                {isImageHovered && (
                  <div className="absolute inset-0 pointer-events-none">
                    {[...Array(8)].map((_, i) => (
                      <div
                        key={i}
                        className="bubble absolute"
                        style={{
                          width: `${Math.random() * 10 + 5}px`,
                          height: `${Math.random() * 10 + 5}px`,
                          left: `${Math.random() * 100}%`,
                          bottom: "10%",
                          animation: `float-up ${
                            Math.random() * 2 + 2
                          }s ease-out forwards`,
                        }}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Decorative Ring */}
              <div
                className={`absolute inset-0 rounded-full border-2 border-ocean-300/50 transition-all duration-500 ${
                  isImageHovered ? "scale-110 opacity-100" : "scale-100 opacity-50"
                }`}
                style={{ margin: "-8px" }}
              />

              {/* Second Ring */}
              <div
                className={`absolute inset-0 rounded-full border border-ocean-200/30 transition-all duration-700 ${
                  isImageHovered ? "scale-125 opacity-100" : "scale-105 opacity-30"
                }`}
                style={{ margin: "-16px" }}
              />
            </div>
          </div>

          {/* Introduction Text */}
          <div
            className={`transition-all duration-700 delay-300 ${
              isVisible
                ? "opacity-100 translate-x-0"
                : "opacity-0 translate-x-12"
            }`}
          >
            <p className="text-ocean-400 font-medium mb-3 text-lg">{greeting}</p>
            <div className="text-ocean-700 leading-relaxed mb-8 space-y-4">
              {description.split("\n\n").map((paragraph, index) => (
                <p key={index} className="text-base">
                  {paragraph}
                </p>
              ))}
            </div>

            {/* Highlights with ocean theme */}
            <div className="space-y-4">
              {highlights.map((item, index) => (
                <div
                  key={index}
                  className={`flex items-center gap-4 transition-all duration-500 ${
                    isVisible
                      ? "opacity-100 translate-x-0"
                      : "opacity-0 translate-x-8"
                  }`}
                  style={{ transitionDelay: `${400 + index * 100}ms` }}
                >
                  <span className="flex-shrink-0 w-3 h-3 rounded-full bg-gradient-to-br from-ocean-300 to-ocean-500" />
                  <span className="text-ocean-600 font-medium">{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
