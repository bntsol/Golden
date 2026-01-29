'use client';

import { useState } from 'react';

const presets = [
  { icon: 'hiking', label: 'Map hiking trails' },
  { icon: 'map', label: 'Create a custom map' },
  { icon: 'traffic', label: 'Display live traffic' },
  { icon: 'city', label: 'Inform urban planning' },
  { icon: 'sparkle', label: 'Surprise me' },
];

// SVG 아이콘 컴포넌트 - currentColor 사용으로 부모 text-color 상속
function PresetIcon({ type }: { type: string }) {
  const iconClass = "w-4 h-4";

  switch (type) {
    case 'hiking':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={iconClass}>
          <path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7"/>
        </svg>
      );
    case 'map':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={iconClass}>
          <path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/>
        </svg>
      );
    case 'traffic':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={iconClass}>
          <path d="M20 10h-3V8.86c1.72-.45 3-2 3-3.86h-3V4c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v1H4c0 1.86 1.28 3.41 3 3.86V10H4c0 1.86 1.28 3.41 3 3.86V15H4c0 1.86 1.28 3.41 3 3.86V20c0 .55.45 1 1 1h8c.55 0 1-.45 1-1v-1.14c1.72-.45 3-2 3-3.86h-3v-1.14c1.72-.45 3-2 3-3.86zm-8 9c-1.11 0-2-.9-2-2s.89-2 2-2 2 .9 2 2-.89 2-2 2zm0-5c-1.11 0-2-.9-2-2s.89-2 2-2 2 .9 2 2-.89 2-2 2zm0-5c-1.11 0-2-.9-2-2s.89-2 2-2 2 .89 2 2-.89 2-2 2z"/>
        </svg>
      );
    case 'city':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={iconClass}>
          <path d="M15 11V5l-3-3-3 3v2H3v14h18V11h-6zm-8 8H5v-2h2v2zm0-4H5v-2h2v2zm0-4H5V9h2v2zm6 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2zm6 12h-2v-2h2v2zm0-4h-2v-2h2v2z"/>
        </svg>
      );
    case 'sparkle':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={iconClass}>
          <path d="M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25L19 15z"/>
        </svg>
      );
    default:
      return null;
  }
}

export default function ChatOverlay() {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = () => {
    if (inputValue.trim()) {
      console.log('Query:', inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none">
      {/* 컨테이너 박스 - Brave 스타일 밝은 테마 */}
      <div className="pointer-events-auto w-full max-w-[680px] mx-4 bg-white rounded-3xl p-8 pb-6 shadow-xl">
        {/* 제목 */}
        <h2 className="text-[#1c1c1d] text-2xl font-normal leading-7 text-center mb-6">
          오늘은 어떤 지도가 필요하신가요?
        </h2>

        {/* 검색창 - Brave 스타일 pill 형태 */}
        <div className="relative mb-6">
          <div className="relative bg-white rounded-[30px] shadow-[0_2px_8px_rgba(0,0,0,0.08)] border border-gray-200">
            <textarea
              className="w-full h-[58px] py-4 pl-4 pr-16 text-base leading-6 text-[#1c1c1d] bg-transparent resize-none outline-none placeholder:text-gray-400"
              placeholder="Ask anything, find anything..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            {/* 제출 버튼 - Brave 스타일 */}
            <button
              type="button"
              className="absolute right-2 top-1/2 -translate-y-1/2 h-10 px-4 flex items-center gap-1.5 bg-gradient-to-r from-[#7c3aed] to-[#a855f7] hover:from-[#6d28d9] hover:to-[#9333ea] rounded-full text-white text-sm font-medium cursor-pointer transition-all duration-200"
              onClick={handleSubmit}
              aria-label="Ask"
            >
              <svg
                viewBox="0 0 24 24"
                fill="currentColor"
                className="w-4 h-4"
              >
                <path d="M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5z"/>
              </svg>
              <span>Ask</span>
            </button>
          </div>
        </div>

        {/* 프리셋 칩 버튼 - Brave 스타일 밝은 테마 */}
        <div className="flex flex-wrap gap-2 justify-center mb-5">
          {presets.map((preset) => (
            <button
              key={preset.label}
              type="button"
              className="inline-flex items-center gap-2 h-9 py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 hover:text-gray-900 text-sm font-medium rounded-full cursor-pointer transition-all duration-200"
              onClick={() => setInputValue(preset.label)}
            >
              <PresetIcon type={preset.icon} />
              <span>{preset.label}</span>
            </button>
          ))}
        </div>

        {/* 푸터 */}
        <p className="text-gray-500 text-xs leading-4 text-center">
          <a href="https://cloud.google.com/vertex-ai" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            Vertex AI
          </a>
          {' '}및 Gemini를 사용하여 빌드되었습니다. 이 서비스를 이용하려면 만 18세 이상이어야 합니다.
          <br className="hidden sm:block" />
          민감하거나 기밀이거나 개인적인 정보를 입력하지 마세요.
        </p>
      </div>
    </div>
  );
}
