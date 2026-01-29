import PageVisitsCard from "@/components/PageVisitsCard";
import SocialTrafficCard from "@/components/SocialTrafficCard";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f5f7fa] p-8">
      <div className="flex gap-6">
        <div className="flex-[2]">
          <PageVisitsCard />
        </div>
        <div className="flex-1">
          <SocialTrafficCard />
        </div>
      </div>
    </div>
  );
}
