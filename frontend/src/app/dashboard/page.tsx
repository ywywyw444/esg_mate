'use client';

import React from 'react';

export default function DashboardPage() {
  const handleButtonClick = (action: string) => {
    console.log(`${action} 버튼 클릭됨`);
    // 여기에 각 버튼별 동작 로직 추가
  };


  
  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-4">
        {/* 기업명 버튼 */}
        <button
          onClick={() => handleButtonClick('기업명')}
          className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium py-3 px-6 rounded-lg border border-black transition-colors duration-200 shadow-md"
        >
          기업명
        </button>
        {/* 재무정보(표) 버튼 */}
        <button
          onClick={() => handleButtonClick('재무정보')}
          className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium py-4 px-6 rounded-lg border border-black transition-colors duration-200 shadow-md"
        >
          재무정보(표)
        </button>

        {/* 중대성평가 결과 버튼 */}
        <button
          onClick={() => handleButtonClick('중대성평가')}
          className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium py-4 px-6 rounded-lg border border-black transition-colors duration-200 shadow-md"
        >
          중대성평가 결과
        </button>

        {/* GRI 보고서 작성 결과 버튼 */}
        <button
          onClick={() => handleButtonClick('GRI보고서')}
          className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium py-4 px-6 rounded-lg border border-black transition-colors duration-200 shadow-md"
        >
          GRI 보고서 작성 결과
        </button>

        {/* TCFD보고서 작성 결과 버튼 */}
        <button
          onClick={() => handleButtonClick('TCFD보고서')}
          className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium py-4 px-6 rounded-lg border border-black transition-colors duration-200 shadow-md"
        >
          TCFD보고서 작성 결과
        </button>
      </div>
    </div>
  );
}
