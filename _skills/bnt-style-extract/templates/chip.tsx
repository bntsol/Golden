/**
 * Chip/Tag Component Template
 *
 * Extracted style placeholders:
 * - [#bg]: Background color
 * - [#bg-hover]: Hover background color
 * - [#text]: Text color
 * - [#text-hover]: Hover text color
 * - [py]: Vertical padding
 * - [px]: Horizontal padding
 * - [radius]: Border radius (usually rounded-full or rounded-3xl)
 * - [font-size]: Font size
 */

import React from 'react';

interface ChipProps {
  children: React.ReactNode;
  icon?: React.ReactNode;
  onClick?: () => void;
  onRemove?: () => void;
  selected?: boolean;
  disabled?: boolean;
  className?: string;
}

export function Chip({
  children,
  icon,
  onClick,
  onRemove,
  selected = false,
  disabled = false,
  className = '',
}: ChipProps) {
  const isClickable = onClick && !disabled;

  return (
    <span
      className={`
        inline-flex items-center gap-2
        bg-[#bg] ${isClickable ? 'hover:bg-[#bg-hover]' : ''}
        text-[#text] ${isClickable ? 'hover:text-[#text-hover]' : ''}
        [py] [px] [radius] [font-size]
        font-medium
        transition-all duration-200
        ${isClickable ? 'cursor-pointer' : ''}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        ${selected ? 'ring-2 ring-[#text]' : ''}
        ${className}
      `.trim().replace(/\s+/g, ' ')}
      onClick={isClickable ? onClick : undefined}
      role={isClickable ? 'button' : undefined}
      tabIndex={isClickable ? 0 : undefined}
    >
      {icon && <span className="w-4 h-4">{icon}</span>}
      <span>{children}</span>
      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-1 hover:text-white transition-colors"
          aria-label="Remove"
        >
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  );
}

// Chip group for multiple selection
interface ChipGroupProps {
  children: React.ReactNode;
  className?: string;
}

export function ChipGroup({ children, className = '' }: ChipGroupProps) {
  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {children}
    </div>
  );
}

// Badge variant (smaller, non-interactive)
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  className?: string;
}

export function Badge({
  children,
  variant = 'default',
  className = '',
}: BadgeProps) {
  const variants = {
    default: 'bg-[#bg] text-[#text]',
    success: 'bg-green-500/20 text-green-400',
    warning: 'bg-yellow-500/20 text-yellow-400',
    error: 'bg-red-500/20 text-red-400',
    info: 'bg-blue-500/20 text-blue-400',
  };

  return (
    <span
      className={`
        inline-flex items-center
        px-2.5 py-0.5
        rounded-full text-xs font-medium
        ${variants[variant]}
        ${className}
      `.trim().replace(/\s+/g, ' ')}
    >
      {children}
    </span>
  );
}

export default Chip;
