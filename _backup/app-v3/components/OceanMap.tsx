'use client';

import { useState, useEffect } from 'react';
import { Map } from 'react-map-gl/maplibre';

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
    <div className="relative h-screen w-screen">
      {/* 지도 영역 - 전체 화면 */}
      <div className="absolute inset-0">
        <Map
          {...viewState}
          onMove={(evt) => setViewState(evt.viewState)}
          mapStyle={MAP_STYLE}
          style={{ width: '100%', height: '100%' }}
          attributionControl={false}
        />
      </div>
    </div>
  );
}
