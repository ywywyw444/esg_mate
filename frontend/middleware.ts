// frontend/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // 정적/메타/공개 경로는 통과
  const PUBLIC = /^\/(_next\/static|_next\/image|favicon\.ico|robots\.txt|sitemap\.xml|manifest(\.webmanifest|\.json)?|icon.*\.png|apple-touch-icon.*\.png|images|fonts|login|signup|api\/auth)/i;
  if (PUBLIC.test(pathname)) return NextResponse.next();

  // ↓ 여기서부터 너의 인증 로직 (쿠키/토큰 검사 등)
  // 인증 실패 시:
  // return NextResponse.redirect(new URL('/login', req.url));
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static).*)'], // 전체에 적용하되 위에서 PUBLIC으로 제외
};
