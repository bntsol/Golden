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
      {/* 컨테이너 박스 - 어두운 남색 박스 */}
      <div className="pointer-events-auto w-full max-w-[680px] mx-4 bg-[#0d1421] rounded-3xl p-8 pb-6 shadow-2xl">
        {/* 제목 */}
        <h2 className="text-white text-2xl font-normal leading-7 text-center mb-6">
          오늘은 어떤 지도가 필요하신가요?
        </h2>

        {/* 검색창 - textarea 멀티라인 스타일 */}
        <div className="relative mb-6">
          {/* 그라데이션 테두리 wrapper */}
          <div className="gradient-border rounded-3xl">
            <div className="relative bg-[#202124] rounded-[23px]">
              <textarea
                className="w-full h-[140px] p-4 pr-16 pb-14 text-[15px] leading-6 text-white bg-transparent resize-none outline-none placeholder:text-[#86868b]"
                placeholder="Use environmental data to recommend locations for new parks in the area"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit();
                  }
                }}
              />
              {/* 제출 버튼 - 우측 하단 */}
              <button
                type="button"
                className="absolute right-3 bottom-3 w-10 h-10 flex items-center justify-center bg-[#1a73e8] hover:bg-[#1967d2] rounded-full text-white cursor-pointer transition-colors duration-200"
                onClick={handleSubmit}
                aria-label="Submit"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-5 h-5"
                >
                  <path d="M5 12h14M13 5l7 7-7 7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* 프리셋 칩 버튼 - Google 스타일 테두리 있는 반투명 */}
        <div className="flex flex-wrap gap-2 justify-center mb-5">
          {presets.map((preset) => (
            <button
              key={preset.label}
              type="button"
              className="inline-flex items-center gap-2 h-9 py-3 px-4 bg-[#183d79] hover:bg-[#1e4b96] text-[#aecbfa] hover:text-white text-sm font-medium border border-transparent rounded-3xl cursor-pointer transition-all duration-200"
              onClick={() => setInputValue(preset.label)}
            >
              <PresetIcon type={preset.icon} />
              <span>{preset.label}</span>
            </button>
          ))}
        </div>

        {/* 푸터 */}
        <p className="text-[#bdc1c6] text-xs leading-4 text-center">
          <a href="https://cloud.google.com/vertex-ai" className="text-[#8ab4f8] hover:underline" target="_blank" rel="noopener noreferrer">
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
