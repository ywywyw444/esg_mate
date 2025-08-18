import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import PWAInstall from "@/components/PWAInstall";
import SWRegister from "./sw-register";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#0d9488",
  userScalable: false,
  viewportFit: "cover",
};

export const metadata: Metadata = {
  title: "Est Mate - 지속가능성 보고서 작성 도구",
  description: "GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼. 기업의 ESG 보고서 작성과 관리를 지원합니다.",
  keywords: ["ESG", "GRI", "TCFD", "지속가능성", "보고서", "기업", "환경", "사회", "거버넌스"],
  authors: [{ name: "Est Mate Team" }],
  creator: "Est Mate",
  publisher: "Est Mate",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  manifest: "/manifest.json",
  icons: {
    icon: [
      { url: "/icon-192x192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512x512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
  openGraph: {
    title: "Est Mate - 지속가능성 보고서 작성 도구",
    description: "GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼",
    type: "website",
    locale: "ko_KR",
    siteName: "Est Mate",
  },
  twitter: {
    card: "summary_large_image",
    title: "Est Mate - 지속가능성 보고서 작성 도구",
    description: "GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="dark">
      <head>
        <meta name="application-name" content="Est Mate" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Est Mate" />
        <meta name="description" content="GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼" />
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
        <meta name="msapplication-TileColor" content="#0d9488" />
        <meta name="msapplication-tap-highlight" content="no" />
        <meta name="theme-color" content="#0d9488" />
        
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/icon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/icon-16x16.png" />
        <link rel="manifest" href="/manifest.json" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0d9488" />
        <link rel="shortcut icon" href="/favicon.ico" />
        
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:url" content="https://est-mate.vercel.app" />
        <meta name="twitter:title" content="Est Mate - 지속가능성 보고서 작성 도구" />
        <meta name="twitter:description" content="GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼" />
        <meta name="twitter:image" content="https://est-mate.vercel.app/og-image.png" />
        <meta name="twitter:creator" content="@estmate" />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="Est Mate - 지속가능성 보고서 작성 도구" />
        <meta property="og:description" content="GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼" />
        <meta property="og:site_name" content="Est Mate" />
        <meta property="og:url" content="https://est-mate.vercel.app" />
        <meta property="og:image" content="https://est-mate.vercel.app/og-image.png" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-900 text-white`}
      >
        {children}
        <PWAInstall />
        <SWRegister />
      </body>
    </html>
  );
}
