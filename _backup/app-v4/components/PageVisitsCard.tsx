"use client";

interface PageVisitRow {
  pageName: string;
  visitors: number;
  uniqueUsers: number;
  bounceRate: number;
  bounceDirection: "up" | "down";
}

const PAGE_VISIT_DATA: PageVisitRow[] = [
  { pageName: "/argon/", visitors: 4569, uniqueUsers: 340, bounceRate: 46.53, bounceDirection: "up" },
  { pageName: "/argon/index.html", visitors: 3985, uniqueUsers: 319, bounceRate: 46.53, bounceDirection: "down" },
  { pageName: "/argon/charts.html", visitors: 3513, uniqueUsers: 294, bounceRate: 36.49, bounceDirection: "down" },
  { pageName: "/argon/tables.html", visitors: 2050, uniqueUsers: 147, bounceRate: 50.87, bounceDirection: "up" },
  { pageName: "/argon/profile.html", visitors: 1795, uniqueUsers: 190, bounceRate: 46.53, bounceDirection: "up" },
];

function formatNumber(num: number): string {
  return num.toLocaleString("en-US");
}

export default function PageVisitsCard() {
  return (
    <div className="bg-white rounded shadow-sm">
      {/* Card Header */}
      <div className="px-6 py-4 border-b border-[#e9ecef]">
        <h3 className="text-lg font-semibold text-[#32325d]">Page visits</h3>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-[#f6f9fc]">
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                PAGE NAME
              </th>
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                VISITORS
              </th>
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                UNIQUE USERS
              </th>
              <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8898aa]">
                BOUNCE RATE
              </th>
            </tr>
          </thead>
          <tbody>
            {PAGE_VISIT_DATA.map((row, index) => (
              <tr key={index} className="border-t border-[#e9ecef]">
                <td className="px-6 py-3 text-sm text-[#525f7f]">{row.pageName}</td>
                <td className="px-6 py-3 text-sm text-[#525f7f]">{formatNumber(row.visitors)}</td>
                <td className="px-6 py-3 text-sm text-[#525f7f]">{formatNumber(row.uniqueUsers)}</td>
                <td className="px-6 py-3 text-sm text-[#525f7f]">
                  <span className="flex items-center gap-1">
                    {row.bounceDirection === "up" ? (
                      <svg className="w-3 h-3 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 6.414l-3.293 3.293a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="w-3 h-3 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 13.586l3.293-3.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                    {row.bounceRate.toFixed(2).replace(".", ",")}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
