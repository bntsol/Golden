'use client';

import { useState, useEffect } from 'react';
import { Map } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

const INITIAL_VIEW_STATE = {
  longitude: 128.5,
  latitude: 36.0,
  zoom: 6,
  pitch: 0,
  bearing: 0,
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json';

export default function OceanMap() {
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-slate-950">
        <div className="text-slate-400">지도 로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-screen">
      {/* 지도 영역 */}
      <div className="relative flex-1">
        <Map
          {...viewState}
          onMove={(evt) => setViewState(evt.viewState)}
          mapStyle={MAP_STYLE}
          style={{ width: '100%', height: '100%' }}
          attributionControl={false} 
        />
      </div>

      {/* 채팅 패널 */}
      <div className="w-[400px] bg-slate-900 border-l border-slate-700 flex flex-col">
        {/* 헤더 */}
        <div className="p-4 border-b border-slate-700">
          <h2 className="text-lg font-semibold text-white text-center">AI 어시스턴트</h2>
        </div>

        {/* 메시지 영역 (빈 박스) */}
        <div className="flex-1 p-4">
          {/* 추후 메시지 구현 */}
        </div>

        {/* 입력 영역 (빈 박스) */}
        <div className="p-4 border-t border-slate-700">
          {/* 추후 입력창 구현 */}
        </div>
      </div>
    </div>
  );
}