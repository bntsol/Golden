import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "My Portfolio",
  description: "Welcome to my personal website",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="scroll-smooth">
      <body
        className="bg-neutral-50 text-neutral-800"
        style={{ fontFamily: "'Noto Sans KR', sans-serif" }}
      >
        {children}
      </body>
    </html>
  );
}
