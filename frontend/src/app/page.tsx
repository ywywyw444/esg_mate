'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const portfolioItems = [
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M20 18c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H1c-.6 0-1 .4-1 1s.4 1 1 1h22c.6 0 1-.4 1-1s-.4-1-1-1h-3zM4 6h16v10H4V6z"/>
        </svg>
      ),
      title: "who am i?",
      description: "나는 태영이야"
    },
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      ),
      title: "재무대시보드",
      description: "유가증권시장 내역을 나랑 살펴볼래? ㅋㅋ"
    },
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
      ),
      title: "esg 공시 챗봇",
      description: "esg 공시가 헷갈려?"
    },
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      ),
      title: "지구가 아파한대!!",
      description: "우리나라가 어떻게 변해가는지 알아볼까?"
    },
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      ),
      title: "TCFD 기준으로 SR작성해볼까?",
      description: "SR을 ai와 함께 작성해보기"
    },
    {
      icon: (
        <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      ),
      title: "나한테 사진 찍힐래?",
      description: "사진찍는거 좋아하는데 내 필름으로 들어올래?"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* 네비게이션 */}
      <nav className="absolute top-0 left-0 right-0 z-50 bg-transparent">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* 햄버거 메뉴 */}
            <div className="flex items-center">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-white hover:text-gray-300 focus:outline-none"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
            
            {/* 중앙 로고 */}
            <div className="flex-1 flex justify-center">
              <h1 className="text-white text-xl font-medium">정태영의 인생사</h1>
            </div>
            
            {/* 우측 메뉴 - 기존 URL들 보존 */}
            <div className="flex items-center space-x-6">
              <Link href="/login" className="text-white hover:text-gray-300 text-sm font-medium">
                LOGIN
              </Link>
              <Link href="/signup" className="text-white hover:text-gray-300 text-sm font-medium">
                SIGNUP
              </Link>
              <button className="text-white hover:text-gray-300">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        {/* 모바일 메뉴 - 기존 URL들 보존 */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-100">
              <Link href="/login" className="text-gray-600 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium">
                LOGIN
              </Link>
              <Link href="/signup" className="text-gray-600 hover:text-gray-900 block px-3 py-2 rounded-md text-base font-medium">
                SIGNUP
              </Link>
            </div>
          </div>
        )}
      </nav>

      {/* 히어로 섹션 - 밤하늘 배경 */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* 배경 그라데이션 */}
        <div className="absolute inset-0 bg-gradient-to-b from-teal-900 via-teal-800 to-teal-700"></div>
        
        {/* 별들 */}
        <div className="absolute inset-0">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 2}s`
              }}
            ></div>
          ))}
        </div>
        
        {/* 달 */}
        <div className="absolute top-20 left-20 w-16 h-16 bg-white rounded-full opacity-80">
          <div className="absolute top-2 left-2 w-12 h-12 bg-teal-900 rounded-full"></div>
        </div>
        
        {/* 산들 */}
        <div className="absolute bottom-0 left-0 right-0">
          <div className="relative h-64">
            {/* 첫 번째 산 */}
            <div className="absolute bottom-0 left-0 w-0 h-0 border-l-[200px] border-r-[200px] border-b-[120px] border-l-transparent border-r-transparent border-b-gray-300"></div>
            {/* 두 번째 산 */}
            <div className="absolute bottom-0 left-1/4 w-0 h-0 border-l-[150px] border-r-[150px] border-b-[100px] border-l-transparent border-r-transparent border-b-gray-400"></div>
            {/* 세 번째 산 */}
            <div className="absolute bottom-0 right-1/4 w-0 h-0 border-l-[180px] border-r-[180px] border-b-[110px] border-l-transparent border-r-transparent border-b-gray-300"></div>
            {/* 네 번째 산 */}
            <div className="absolute bottom-0 right-0 w-0 h-0 border-l-[160px] border-r-[160px] border-b-[90px] border-l-transparent border-r-transparent border-b-gray-400"></div>
          </div>
        </div>
        
        {/* 새들 */}
        <div className="absolute top-1/3 right-1/4">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="absolute text-white opacity-80 animate-bounce"
              style={{
                left: `${i * 20}px`,
                top: `${i * 10}px`,
                animationDelay: `${i * 0.5}s`
              }}
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L9 9H2l5.5 4L5 20l7-5 7 5-2.5-7L22 9h-7l-3-7z"/>
              </svg>
            </div>
          ))}
        </div>
        
        {/* 텍스트 오버레이 */}
        <div className="relative z-10 text-center text-white px-4">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          안되면 되게하라<br />
            하고자 하는 일에 후회하지 않도록 최선을 다하자
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 max-w-2xl mx-auto mb-8">
            Click here to add your own text and edit me.
          </p>
          
          {/* CTA 버튼들 - 기존 URL들 보존 */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/login" className="bg-white text-teal-900 hover:bg-gray-100 px-8 py-4 rounded-lg text-lg font-semibold transition-colors duration-200">
              로그인하기
            </Link>
            <Link href="/signup" className="border-2 border-white text-white hover:bg-white hover:text-teal-900 px-8 py-4 rounded-lg text-lg font-semibold transition-colors duration-200">
              회원가입
            </Link>
          </div>
        </div>
      </section>

      {/* 포트폴리오 섹션 */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              I am a positive person.
            </h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {portfolioItems.map((item, index) => (
              <div key={index} className="bg-gray-100 rounded-lg p-8 shadow-lg transform hover:scale-105 transition-transform duration-300">
                <div className="text-center mb-6">
                  <div className="text-gray-600 mb-4">
                    {item.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    {item.title}
                  </h3>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed mb-6">
                  {item.description}
                </p>
                <div className="text-center">
                  <button className="border-2 border-blue-400 text-blue-600 hover:bg-blue-400 hover:text-white px-6 py-2 rounded-lg transition-colors duration-200 font-medium">
                    MORE
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 추가 섹션 - 기존 기능들 소개 */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Available Services
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              현재 사용 가능한 서비스들을 확인해보세요.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* 로그인 서비스 */}
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">로그인</h3>
                <p className="text-gray-600 text-sm mb-4">사용자 인증 서비스</p>
                <Link href="/login" className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                  바로가기 →
                </Link>
              </div>
            </div>

            {/* 회원가입 서비스 */}
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">회원가입</h3>
                <p className="text-gray-600 text-sm mb-4">새 계정 생성</p>
                <Link href="/signup" className="text-green-600 hover:text-green-700 font-medium text-sm">
                  바로가기 →
                </Link>
              </div>
            </div>

            {/* API 서비스 */}
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-center">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">API Gateway</h3>
                <p className="text-gray-600 text-sm mb-4">마이크로서비스 통합</p>
                <a href="http://localhost:8080/docs" target="_blank" rel="noopener noreferrer" className="text-purple-600 hover:text-purple-700 font-medium text-sm">
                  API 문서 →
                </a>
              </div>
            </div>

            {/* 헬스 체크 */}
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="text-center">
                <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">시스템 상태</h3>
                <p className="text-gray-600 text-sm mb-4">서비스 헬스 체크</p>
                <a href="http://localhost:8080/health" target="_blank" rel="noopener noreferrer" className="text-red-600 hover:text-red-700 font-medium text-sm">
                  상태 확인 →
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 푸터 */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">정태영의 인생사</h3>
              <p className="text-gray-400">
                정태영의 꿈과 희망이 가득찬 이곳
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">서비스</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/login" className="hover:text-white">로그인</Link></li>
                <li><Link href="/signup" className="hover:text-white">회원가입</Link></li>
                <li><a href="http://localhost:8080/docs" target="_blank" rel="noopener noreferrer" className="hover:text-white">API 문서</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">시스템</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="http://localhost:8080/health" target="_blank" rel="noopener noreferrer" className="hover:text-white">헬스 체크</a></li>
                <li><a href="http://localhost:8080/" target="_blank" rel="noopener noreferrer" className="hover:text-white">Gateway API</a></li>
                <li><a href="http://localhost:3000" className="hover:text-white">프론트엔드</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">연락처</h4>
              <ul className="space-y-2 text-gray-400">
                <li>jty000308@naver.com</li>
                <li>010-3880-8322</li>
                <li>서울특별시</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Portfolio. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
