"use client";

import { useEffect, useState } from "react";

interface Bubble {
  id: number;
  size: number;
  left: number;
  duration: number;
  delay: number;
}

interface BubbleEffectProps {
  count?: number;
  minSize?: number;
  maxSize?: number;
  minDuration?: number;
  maxDuration?: number;
}

export default function BubbleEffect({
  count = 10,
  minSize = 4,
  maxSize = 20,
  minDuration = 8,
  maxDuration = 15,
}: BubbleEffectProps) {
  const [bubbles, setBubbles] = useState<Bubble[]>([]);

  useEffect(() => {
    const generateBubbles = () => {
      const newBubbles: Bubble[] = [];
      for (let i = 0; i < count; i++) {
        newBubbles.push({
          id: i,
          size: Math.random() * (maxSize - minSize) + minSize,
          left: Math.random() * 100,
          duration: Math.random() * (maxDuration - minDuration) + minDuration,
          delay: Math.random() * 5,
        });
      }
      setBubbles(newBubbles);
    };

    generateBubbles();
  }, [count, minSize, maxSize, minDuration, maxDuration]);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-10">
      {bubbles.map((bubble) => (
        <div
          key={bubble.id}
          className="bubble"
          style={{
            width: `${bubble.size}px`,
            height: `${bubble.size}px`,
            left: `${bubble.left}%`,
            bottom: "-50px",
            animation: `float-up ${bubble.duration}s ease-in-out ${bubble.delay}s infinite`,
            willChange: "transform, opacity",
          }}
        />
      ))}
    </div>
  );
}
