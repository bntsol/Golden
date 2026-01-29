"use client";

import Image from "next/image";
import { useState } from "react";

interface UnderwaterCardProps {
  image: string;
  title: string;
  description: string;
  index: number;
  onClick: () => void;
}

export default function UnderwaterCard({
  image,
  title,
  description,
  index,
  onClick,
}: UnderwaterCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="group relative overflow-hidden rounded-2xl cursor-pointer hover-glow"
      style={{
        animationDelay: `${index * 0.1}s`,
      }}
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden">
        <Image
          src={image}
          alt={title}
          fill
          quality={80}
          className={`object-cover transition-transform duration-500 ${
            isHovered ? "scale-110" : "scale-100"
          }`}
          sizes="(max-width: 768px) 100vw, 33vw"
        />

        {/* Gradient Overlay */}
        <div
          className={`absolute inset-0 transition-opacity duration-300 ${
            isHovered ? "opacity-70" : "opacity-40"
          }`}
          style={{
            background:
              "linear-gradient(to top, rgba(5, 25, 35, 0.9) 0%, rgba(5, 25, 35, 0.3) 50%, transparent 100%)",
          }}
        />

        {/* Bubble effect on hover */}
        {isHovered && (
          <div className="absolute inset-0 pointer-events-none">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="bubble absolute"
                style={{
                  width: `${Math.random() * 8 + 4}px`,
                  height: `${Math.random() * 8 + 4}px`,
                  left: `${Math.random() * 100}%`,
                  bottom: "0",
                  animation: `float-up ${Math.random() * 2 + 2}s ease-out forwards`,
                }}
              />
            ))}
          </div>
        )}

        {/* Number Badge */}
        <div className="absolute top-4 left-4 w-10 h-10 rounded-full bg-ocean-400/80 backdrop-blur-sm flex items-center justify-center text-white font-semibold text-lg z-10">
          {String(index + 1).padStart(2, "0")}
        </div>
      </div>

      {/* Content */}
      <div className="absolute bottom-0 left-0 right-0 p-5 z-10">
        <h3 className="text-xl font-semibold text-white mb-1 text-glow">
          {title}
        </h3>
        <p
          className={`text-aqua/80 text-sm transition-all duration-300 ${
            isHovered ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"
          }`}
        >
          {description}
        </p>
      </div>

      {/* Hover Border Glow */}
      <div
        className={`absolute inset-0 rounded-2xl pointer-events-none transition-opacity duration-300 ${
          isHovered ? "opacity-100" : "opacity-0"
        }`}
        style={{
          boxShadow: "inset 0 0 30px rgba(8, 131, 149, 0.5)",
        }}
      />
    </div>
  );
}
