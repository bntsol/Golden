interface WaveOverlayProps {
  position: "top" | "bottom";
  color?: string;
  animate?: boolean;
  flip?: boolean;
}

export default function WaveOverlay({
  position,
  color = "#0a4d68",
  animate = true,
  flip = false,
}: WaveOverlayProps) {
  const positionClasses = position === "top" ? "top-0" : "bottom-0";
  const flipTransform = flip ? "rotate-180" : "";

  return (
    <div
      className={`absolute ${positionClasses} left-0 right-0 overflow-hidden pointer-events-none z-20`}
      style={{ height: "80px" }}
    >
      <svg
        viewBox="0 0 1200 120"
        preserveAspectRatio="none"
        className={`absolute w-[200%] h-full ${flipTransform}`}
        style={{
          animation: animate ? "wave 5s ease-in-out infinite" : "none",
          willChange: animate ? "transform" : "auto",
        }}
      >
        <path
          d="M0,60 C150,90 350,30 600,60 C850,90 1050,30 1200,60 L1200,120 L0,120 Z"
          fill={color}
          fillOpacity="0.8"
        />
        <path
          d="M0,80 C200,50 400,100 600,80 C800,60 1000,100 1200,80 L1200,120 L0,120 Z"
          fill={color}
          fillOpacity="0.5"
        />
      </svg>
    </div>
  );
}
