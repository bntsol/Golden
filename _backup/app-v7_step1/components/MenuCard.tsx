interface MenuCardProps {
  emoji: string;
  name: string;
  description: string;
  price: string;
}

export default function MenuCard({ emoji, name, description, price }: MenuCardProps) {
  return (
    <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow text-center">
      <span className="text-5xl block mb-5">{emoji}</span>
      <h3 className="text-lg font-medium mb-2">{name}</h3>
      <p className="text-stone-400 text-sm leading-relaxed mb-4">{description}</p>
      <p className="text-amber-700 font-medium">{price}</p>
    </div>
  );
}
