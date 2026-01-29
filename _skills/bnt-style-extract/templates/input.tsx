/**
 * Input Component Template
 *
 * Extracted style placeholders:
 * - [#bg]: Background color
 * - [#text]: Text color
 * - [#placeholder]: Placeholder text color
 * - [#border]: Border color
 * - [#border-focus]: Focus border color
 * - [padding]: Padding classes
 * - [radius]: Border radius
 */

import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export function Input({
  label,
  error,
  icon,
  className = '',
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-[#text] mb-2">
          {label}
        </label>
      )}

      <div className="relative">
        {icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#placeholder]">
            {icon}
          </div>
        )}

        <input
          className={`
            w-full
            bg-[#bg] text-[#text]
            border border-[#border]
            focus:border-[#border-focus] focus:ring-1 focus:ring-[#border-focus]
            [padding] [radius]
            outline-none
            placeholder:text-[#placeholder]
            transition-colors duration-200
            ${icon ? 'pl-12' : ''}
            ${error ? 'border-red-500' : ''}
            ${className}
          `.trim().replace(/\s+/g, ' ')}
          {...props}
        />
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}

// Textarea variant
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export function Textarea({
  label,
  error,
  className = '',
  ...props
}: TextareaProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-[#text] mb-2">
          {label}
        </label>
      )}

      <textarea
        className={`
          w-full min-h-[120px]
          bg-[#bg] text-[#text]
          border border-[#border]
          focus:border-[#border-focus] focus:ring-1 focus:ring-[#border-focus]
          [padding] [radius]
          outline-none resize-none
          placeholder:text-[#placeholder]
          transition-colors duration-200
          ${error ? 'border-red-500' : ''}
          ${className}
        `.trim().replace(/\s+/g, ' ')}
        {...props}
      />

      {error && (
        <p className="mt-2 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}

// Input with gradient border
export function GradientInput({
  className = '',
  ...props
}: InputProps) {
  return (
    <div className="p-[1px] rounded-3xl bg-gradient-to-r from-[#gradient-start] to-[#gradient-end]">
      <div className="bg-[#bg] rounded-[calc(1.5rem-1px)]">
        <input
          className={`
            w-full p-4
            bg-transparent text-[#text]
            outline-none
            placeholder:text-[#placeholder]
            ${className}
          `.trim().replace(/\s+/g, ' ')}
          {...props}
        />
      </div>
    </div>
  );
}

export default Input;
