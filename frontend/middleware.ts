// frontend/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// 미들웨어가 적용될 "대상"을 좁혀서, 정적/메타 파일은 아예 미들웨어를 타지 않게 함
export const config = {
  matcher: [
    // ↓ 아래에 나열한 것들을 제외한 모든 경로에만 미들웨어 적용
    '/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|manifest.json|manifest.webmanifest|site.webmanifest|icon.*\\.png|apple-touch-icon.*\\.png|images|fonts|api/auth|login|signup).*)',
  ],
};

export function middleware(req: NextRequest) {
  // 프리플라이트/HEAD는 바로 통과
  if (req.method === 'OPTIONS' || req.method === 'HEAD') {
    return NextResponse.next();
  }

  // 여기서부터 필요하면 인증 로직 추가(현재는 모두 통과)
  return NextResponse.next();
}
