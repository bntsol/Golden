export default function PricingPage() {
  const plans = [
    {
      name: "Basic Plan",
      description: "Ideal for small businesses",
      price: "$19.99",
      features: ["10 Users", "Basic Features", "24/7 Support"],
      buttonColor: "bg-[#3b82f6] hover:bg-[#2563eb]",
      barGradient: "from-[#93c5fd] via-[#60a5fa] to-[#3b82f6]",
      checkColor: "text-[#3b82f6]"
    },
    {
      name: "Pro Plan",
      description: "Perfect for growing businesses",
      price: "$49.99",
      features: ["25 Users", "Advanced Features", "24/7 Support"],
      buttonColor: "bg-[#22c55e] hover:bg-[#16a34a]",
      barGradient: "from-[#86efac] via-[#4ade80] to-[#22c55e]",
      checkColor: "text-[#22c55e]"
    },
    {
      name: "Enterprise Plan",
      description: "For large-scale enterprises",
      price: "$99.99",
      features: ["Unlimited Users", "Premium Features", "24/7 Priority Support"],
      buttonColor: "bg-[#a855f7] hover:bg-[#9333ea]",
      barGradient: "from-[#d8b4fe] via-[#c084fc] to-[#a855f7]",
      checkColor: "text-[#a855f7]"
    }
  ];

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#f3f4f6] p-6">
      <div className="flex gap-[40px]">
        {plans.map((plan, index) => (
          <div
            key={index}
            className="bg-white rounded-xl shadow-[0_4px_24px_rgba(0,0,0,0.08)] overflow-hidden w-[295px]"
          >
            <div className={`h-[5px] bg-gradient-to-r ${plan.barGradient}`} />
            <div className="px-[30px] pt-[17px] pb-[52px]">
              <h2 className="text-[28px] font-bold text-gray-900 mb-[2px] leading-[1.3]">{plan.name}</h2>
              <p className="text-sm text-gray-500 mb-[32px]">{plan.description}</p>

              <div className="mb-[29px]">
                <span className="text-[44px] font-extrabold text-gray-900 leading-none">{plan.price}</span>
              </div>

              <ul className="space-y-[8px] mb-[82px]">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-2.5">
                    <svg className={`w-[16px] h-[16px] flex-shrink-0 ${plan.checkColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-[15px] text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <button className={`w-full py-3.5 px-6 rounded-full text-[15px] text-white font-semibold transition-colors ${plan.buttonColor}`}>
                Select Plan
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
