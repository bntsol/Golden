/**
 * Button Component Template
 *
 * Extracted style placeholders:
 * - [#bg]: Background color
 * - [#bg-hover]: Hover background color
 * - [#text]: Text color
 * - [#text-hover]: Hover text color
 * - [py]: Vertical padding (e.g., py-3)
 * - [px]: Horizontal padding (e.g., px-6)
 * - [radius]: Border radius (e.g., rounded-lg)
 * - [font-size]: Font size (e.g., text-sm)
 * - [font-weight]: Font weight (e.g., font-medium)
 */

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = `
    inline-flex items-center justify-center
    font-medium
    transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  const variants = {
    primary: `
      bg-[#bg] hover:bg-[#bg-hover]
      text-[#text] hover:text-[#text-hover]
    `,
    secondary: `
      bg-transparent hover:bg-[#bg-hover]
      text-[#text] hover:text-[#text-hover]
      border border-[#border] hover:border-transparent
    `,
    ghost: `
      bg-transparent hover:bg-white/10
      text-[#text] hover:text-white
    `,
  };

  const sizes = {
    sm: 'py-2 px-4 text-sm [radius]',
    md: '[py] [px] [font-size] [radius]',
    lg: 'py-4 px-8 text-base [radius]',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`
        .trim()
        .replace(/\s+/g, ' ')}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
