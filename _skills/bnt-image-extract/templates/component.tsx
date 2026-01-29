/**
 * Base Component Template
 *
 * Replace placeholders with extracted values:
 * - [#bg-color]: Background color hex
 * - [#text-color]: Text color hex
 * - [padding]: Tailwind padding classes
 * - [radius]: Tailwind border-radius class
 */

import React from 'react';

interface ComponentProps {
  children: React.ReactNode;
  className?: string;
}

export function Component({ children, className = '' }: ComponentProps) {
  return (
    <div
      className={`
        bg-[#bg-color]
        text-[#text-color]
        [padding]
        [radius]
        ${className}
      `.trim().replace(/\s+/g, ' ')}
    >
      {children}
    </div>
  );
}

export default Component;
