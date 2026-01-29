"use client";

import { useState } from 'react';

interface CalendarEvent {
  id: string;
  title: string;
  time: string;
  date: number;
  nextMonth?: boolean;
}

const EVENTS: CalendarEvent[] = [
  { id: '1', title: 'Design review', time: '10AM', date: 3 },
  { id: '2', title: 'Sales meeting', time: '2PM', date: 3 },
  { id: '3', title: 'Date night', time: '6PM', date: 7 },
  { id: '4', title: "Sam's birthday party", time: '2PM', date: 12 },
  { id: '5', title: 'Maple syrup museum', time: '3PM', date: 22 },
  { id: '6', title: 'Hockey game', time: '7PM', date: 22 },
  { id: '7', title: 'Cinema with friends', time: '9PM', date: 4, nextMonth: true },
];

const DAYS_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export default function Calendar() {
  const [showDropdown, setShowDropdown] = useState(true);

  const year = 2022;
  const month = 0; // January
  const monthYear = 'January 2022';
  const selectedDay = 12;

  // Generate calendar grid
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const startOffset = firstDay === 0 ? 6 : firstDay - 1;

  const calendarDays: number[] = [];
  for (let i = 0; i < startOffset; i++) {
    calendarDays.unshift(new Date(year, month, -i).getDate());
  }
  for (let i = 1; i <= daysInMonth; i++) {
    calendarDays.push(i);
  }
  while (calendarDays.length < 42) {
    calendarDays.push(calendarDays.length - startOffset - daysInMonth + 1);
  }

  const getEventsForDay = (day: number, isCurrentMonth: boolean, isNextMonth: boolean) => {
    return EVENTS.filter(e => {
      if (e.nextMonth) return isNextMonth && e.date === day;
      return isCurrentMonth && e.date === day;
    });
  };

  return (
    <div className="w-full min-h-screen bg-white flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900">{monthYear}</h1>

        <div className="flex items-center gap-3">
          {/* Today navigation */}
          <div className="flex items-center border border-gray-300 rounded-md overflow-hidden">
            <button className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 border-r border-gray-300">
              &lt;
            </button>
            <span className="px-4 py-1.5 text-sm font-medium text-gray-700">Today</span>
            <button className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 border-l border-gray-300">
              &gt;
            </button>
          </div>

          {/* Month view dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="px-4 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center gap-2"
            >
              Month view
              <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {showDropdown && (
              <div className="absolute right-0 mt-1 w-36 bg-white border border-gray-200 rounded-md shadow-lg z-30 py-1">
                <button className="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100">Day view</button>
                <button className="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100">Week view</button>
                <button className="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 font-medium">Month view</button>
                <button className="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100">Year view</button>
              </div>
            )}
          </div>

          {/* Add event */}
          <button className="px-4 py-1.5 text-sm font-semibold text-white bg-[#4f46e5] rounded-md hover:bg-[#4338ca]">
            Add event
          </button>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="flex-1">
        {/* Day Headers */}
        <div className="grid grid-cols-7 border-b border-gray-200">
          {DAYS_OF_WEEK.map((day) => (
            <div key={day} className="py-2 text-center text-xs font-medium text-gray-500">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar Rows */}
        <div className="grid grid-cols-7 flex-1">
          {calendarDays.map((day, index) => {
            const isCurrentMonth = index >= startOffset && index < startOffset + daysInMonth;
            const isNextMonth = index >= startOffset + daysInMonth;
            const dayEvents = getEventsForDay(day, isCurrentMonth, isNextMonth);
            const isSelected = day === selectedDay && isCurrentMonth;
            const isSat = day === 1 && isCurrentMonth; // Jan 1 is Saturday (red)

            return (
              <div
                key={index}
                className={`min-h-[100px] p-2 border-b border-r border-gray-200 ${
                  !isCurrentMonth ? 'bg-gray-50' : 'bg-white'
                }`}
              >
                <div className={`text-sm ${
                  isSelected
                    ? 'w-7 h-7 flex items-center justify-center rounded-full bg-[#4f46e5] text-white font-semibold'
                    : isSat
                      ? 'text-red-500'
                      : isCurrentMonth
                        ? 'text-gray-900'
                        : 'text-gray-400'
                }`}>
                  {day}
                </div>

                <div className="mt-1 space-y-0.5">
                  {dayEvents.map(event => (
                    <div key={event.id} className="flex items-baseline justify-between">
                      <span className="text-xs text-gray-900 truncate">{event.title}</span>
                      <span className="text-xs text-gray-500 ml-1 shrink-0">{event.time}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
