import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SmartCampus AI — Campus intelligent",
  description: "Orientation universitaire, administration et espaces pédagogiques.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="fr"><body>{children}</body></html>;
}
