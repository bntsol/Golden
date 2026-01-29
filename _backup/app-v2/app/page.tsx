'use client';

import dynamic from "next/dynamic";

// deck.gl/maplibre는 브라우저에서만 동작하므로 SSR 비활성화
const OceanMap = dynamic(() => import("@/components/OceanMap"), {
  ssr: false,
  loading: () => (
    <div className="loading-screen">
      <div className="loading-text">지도 로딩 중...</div>
    </div>
  ),
});

const ChatOverlay = dynamic(() => import("@/components/ChatOverlay"), {
  ssr: false,
});

export default function Home() {
  return (
    <>
      <OceanMap />
      <ChatOverlay />
    </>
  );
}
