'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function SignupPage() {
  const router = useRouter();

  // Form state management
  const [formData, setFormData] = useState({
    company_id: '',
    industry: '',
    email: '',
    name: '',
    age: '',
    auth_id: '',
    auth_pw: ''
  });

  // Form input handler
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Signup form submission
  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    
    // 입력된 데이터를 JSON 형태로 alert에 표시
    const signupData = {
      "회원가입 정보": {
        "회사 ID": formData.company_id,
        "산업": formData.industry,
        "이메일": formData.email,
        "이름": formData.name,
        "나이": formData.age,
        "인증 ID": formData.auth_id,
        "인증 비밀번호": formData.auth_pw
      }
    };
    
    // JSON을 보기 좋게 포맷팅하여 alert에 표시
    alert(JSON.stringify(signupData, null, 2));
    
    // Gateway를 통해 auth-service로 요청
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    console.log(`😂 apiUrl: ${apiUrl}`);

    // ===== [가드 추가] 환경변수 누락 시 사용자 안내 =====
    if (!apiUrl) {
      alert('❌ 서버 주소(NEXT_PUBLIC_API_URL)가 설정되지 않았습니다. 환경변수를 확인해주세요.');
      return;
    }

    axios.post(`${apiUrl}/api/v1/auth/signup`, formData)
      .then(response => {
        console.log('Signup successful:', response.data);
        
        // 성공 메시지 표시
        if (response.data?.success) {
          alert(`✅ ${response.data.message}\n\n이메일: ${response.data.email}\n사용자 ID: ${response.data.user_id}`);
          router.push('/login');
        } else {
          // success 플래그가 없거나 false인 경우
          const msg = response.data?.message || '알 수 없는 응답 형식입니다.';
          alert(`❌ ${msg}`);
        }
      })
      .catch(error => {
        console.error('Signup failed:', error);
        
        // 에러 응답 처리
        const serverMsg =
          error?.response?.data?.message ||
          error?.response?.data?.detail ||
          error?.message ||
          '알 수 없는 오류';
        alert(`❌ 회원가입 실패: ${serverMsg}`);
      });
  };

  // Go back to login page
  const handleBackToLogin = () => {
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-3xl shadow-2xl px-8 py-12">
          {/* Signup Title */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 tracking-tight">
              Sign Up
            </h1>
            <p className="text-gray-600 mt-2">회원가입을 진행해주세요</p>
          </div>

          {/* Signup Form */}
          <form onSubmit={handleSignup} className="space-y-6">
            {/* Company ID Input */}
            <div className="relative">
              <input
                type="text"
                name="company_id"
                value={formData.company_id}
                onChange={handleInputChange}
                placeholder="회사 ID"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Industry Input */}
            <div className="relative">
              <input
                type="text"
                name="industry"
                value={formData.industry}
                onChange={handleInputChange}
                placeholder="산업"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Email Input */}
            <div className="relative">
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="이메일"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Name Input */}
            <div className="relative">
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="이름"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Age Input */}
            <div className="relative">
              <input
                type="text"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                placeholder="나이"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Auth ID Input */}
            <div className="relative">
              <input
                type="text"
                name="auth_id"
                value={formData.auth_id}
                onChange={handleInputChange}
                placeholder="인증 ID"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Auth Password Input */}
            <div className="relative">
              <input
                type="password"
                name="auth_pw"
                value={formData.auth_pw}
                onChange={handleInputChange}
                placeholder="인증 비밀번호"
                className="w-full px-4 py-3 text-gray-800 placeholder-gray-400 bg-gray-50 border border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-all duration-300"
                required
              />
            </div>

            {/* Buttons */}
            <div className="space-y-4 pt-4">
              {/* Sign Up Button */}
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-all duration-200 font-medium text-lg shadow-sm"
              >
                회원가입
              </button>

              {/* Back to Login Button */}
              <button
                type="button"
                onClick={handleBackToLogin}
                className="w-full bg-white border-2 border-gray-300 text-gray-800 py-3 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 font-medium text-lg shadow-sm"
              >
                로그인으로 돌아가기
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
