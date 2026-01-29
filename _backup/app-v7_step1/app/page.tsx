import HeroSection from "@/components/HeroSection";
import MenuCard from "@/components/MenuCard";
import InfoSection from "@/components/InfoSection";

export default function Home() {
  return (
    <div className="min-h-screen">
      <HeroSection />

      <section className="py-12 px-6">
        <h2
          className="text-3xl font-semibold text-center mb-3"
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          Signature Menu
        </h2>
        <p className="text-stone-400 text-center mb-10">
          오늘 하루, 어떤 한 잔을 선택하시겠어요?
        </p>

        <div className="max-w-3xl mx-auto grid grid-cols-3 gap-6">
          <MenuCard
            emoji="☕"
            name="시그니처 라떼"
            description="부드러운 우유 거품 위에 은은한 바닐라 향을 더한 시그니처 메뉴"
            price="₩5,500"
          />
          <MenuCard
            emoji="🥐"
            name="버터 크루아상"
            description="프랑스산 발효 버터로 48시간 숙성한 겹겹이 바삭한 크루아상"
            price="₩4,800"
          />
          <MenuCard
            emoji="🍰"
            name="바스크 치즈케이크"
            description="겉은 캐러멜, 속은 부드러운 크림치즈의 시그니처 디저트와 다이어트 코크"
            price="₩7,500"
          />
        </div>
      </section>

      <InfoSection />
    </div>
  );
}
