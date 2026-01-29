"use client";

import { useState } from "react";
import HeroSection from "@/components/HeroSection";
import MenuCard from "@/components/MenuCard";
import InfoSection from "@/components/InfoSection";
import OrderBar from "@/components/OrderBar";

const menu = [
  {
    emoji: "☕",
    name: "시그니처 라떼",
    description: "부드러운 우유 거품 위에 은은한 바닐라 향을 더한 시그니처 메뉴",
    price: 5500,
  },
  {
    emoji: "🥐",
    name: "버터 크루아상",
    description: "프랑스산 발효 버터로 48시간 숙성한 겹겹이 바삭한 크루아상",
    price: 4800,
  },
  {
    emoji: "🍰",
    name: "바스크 치즈케이크",
    description:
      "겉은 캐러멜, 속은 부드러운 크림치즈의 시그니처 디저트와 다이어트 코크",
    price: 7500,
  },
];

export default function Home() {
  const [quantities, setQuantities] = useState([0, 0, 0]);

  const handleAdd = (index: number) => {
    setQuantities((prev) => {
      const next = [...prev];
      next[index] += 1;
      return next;
    });
  };

  const handleRemove = (index: number) => {
    setQuantities((prev) => {
      const next = [...prev];
      if (next[index] > 0) next[index] -= 1;
      return next;
    });
  };

  const totalCount = quantities.reduce((sum, q) => sum + q, 0);
  const totalPrice = quantities.reduce(
    (sum, q, i) => sum + q * menu[i].price,
    0
  );

  const handleOrder = () => {
    alert(
      `${totalCount}개 메뉴, 총 ${totalPrice.toLocaleString()}원 주문이 완료되었습니다!`
    );
    setQuantities([0, 0, 0]);
  };

  return (
    <div className={`min-h-screen ${totalCount > 0 ? "pb-20" : ""}`}>
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
          {menu.map((item, index) => (
            <MenuCard
              key={item.name}
              emoji={item.emoji}
              name={item.name}
              description={item.description}
              price={item.price}
              quantity={quantities[index]}
              onAdd={() => handleAdd(index)}
              onRemove={() => handleRemove(index)}
            />
          ))}
        </div>
      </section>

      <InfoSection />

      {totalCount > 0 && (
        <OrderBar
          totalCount={totalCount}
          totalPrice={totalPrice}
          onOrder={handleOrder}
        />
      )}
    </div>
  );
}
