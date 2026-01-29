/**
 * Card Component Template
 *
 * Extracted style placeholders:
 * - [#bg]: Background color
 * - [#bg-hover]: Hover background color (for interactive)
 * - [#title]: Title text color
 * - [#text]: Body text color
 * - [padding]: Padding classes
 * - [radius]: Border radius
 * - [shadow]: Box shadow class
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  interactive?: boolean;
  onClick?: () => void;
}

export function Card({
  children,
  className = '',
  interactive = false,
  onClick,
}: CardProps) {
  const baseStyles = `
    bg-[#bg] [radius] [padding] [shadow]
  `;

  const interactiveStyles = interactive
    ? `
      hover:bg-[#bg-hover]
      cursor-pointer
      transition-all duration-200
      hover:shadow-xl hover:-translate-y-1
    `
    : '';

  return (
    <div
      className={`${baseStyles} ${interactiveStyles} ${className}`
        .trim()
        .replace(/\s+/g, ' ')}
      onClick={onClick}
      role={interactive ? 'button' : undefined}
      tabIndex={interactive ? 0 : undefined}
    >
      {children}
    </div>
  );
}

// Card with header
interface CardWithHeaderProps extends CardProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function CardWithHeader({
  title,
  subtitle,
  action,
  children,
  className = '',
  ...props
}: CardWithHeaderProps) {
  return (
    <Card className={className} {...props}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-[#title]">{title}</h3>
          {subtitle && (
            <p className="text-sm text-[#text] mt-1">{subtitle}</p>
          )}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div className="text-[#text]">{children}</div>
    </Card>
  );
}

// Card with image
interface CardWithImageProps extends CardProps {
  image: string;
  imageAlt?: string;
  title: string;
  description?: string;
}

export function CardWithImage({
  image,
  imageAlt = '',
  title,
  description,
  className = '',
  ...props
}: CardWithImageProps) {
  return (
    <Card className={`overflow-hidden p-0 ${className}`} {...props}>
      <img
        src={image}
        alt={imageAlt}
        className="w-full h-48 object-cover"
      />
      <div className="[padding]">
        <h3 className="text-lg font-semibold text-[#title] mb-2">{title}</h3>
        {description && (
          <p className="text-[#text]">{description}</p>
        )}
      </div>
    </Card>
  );
}

// Glass card (glassmorphism)
export function GlassCard({
  children,
  className = '',
  ...props
}: CardProps) {
  return (
    <div
      className={`
        bg-white/10 backdrop-blur-lg
        border border-white/20
        [radius] [padding] [shadow]
        ${className}
      `.trim().replace(/\s+/g, ' ')}
      {...props}
    >
      {children}
    </div>
  );
}

export default Card;
