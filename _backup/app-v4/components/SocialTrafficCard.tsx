"use client";

interface SocialTrafficRow {
  referral: string;
  visitors: number;
  percentage: number;
  barColor: string;
}

const SOCIAL_TRAFFIC_DATA: SocialTrafficRow[] = [
  { referral: "Facebook", visitors: 1480, percentage: 60, barColor: "bg-[#f5365c]" },
  { referral: "Facebook", visitors: 5480, percentage: 70, barColor: "bg-[#2dce89]" },
  { referral: "Google", visitors: 4807, percentage: 80, barColor: "bg-[#5e72e4]" },
  { referral: "Instagram", visitors: 3678, percentage: 75, barColor: "bg-[#5603ad]" },
  { referral: "Twitter", visitors: 2645, percentage: 30, barColor: "bg-[#ffd600]" },
];

function formatNumber(num: number): string {
  return num.toLocaleString("en-US");
}

export default function SocialTrafficCard() {
  return (
    <div className="bg-white rounded shadow-sm">
      {/* Card Header */}
      <div className="px-6 py-4 border-b border-[#e9ecef]">
        <h3 className="text-lg font-semibold text-[#32325d]">Social traffic</h3>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-[#f6f9fc]">
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                REFERRAL
              </th>
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                VISITORS
              </th>
              <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                {/* percentage + bar column */}
              </th>
            </tr>
          </thead>
          <tbody>
            {SOCIAL_TRAFFIC_DATA.map((row, index) => (
              <tr key={index} className="border-t border-[#e9ecef]">
                <td className="px-6 py-3 text-sm text-[#525f7f]">{row.referral}</td>
                <td className="px-6 py-3 text-sm text-[#525f7f]">{formatNumber(row.visitors)}</td>
                <td className="px-6 py-3">
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-[#525f7f] w-10 text-right">{row.percentage}%</span>
                    <div className="w-[100px] h-[5px] bg-[#e9ecef] rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${row.barColor}`}
                        style={{ width: `${row.percentage}%` }}
                      />
                    </div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
