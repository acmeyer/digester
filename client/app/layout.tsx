import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Digester',
  description: 'Summarize urls and files and ask questions about them',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`h-full bg-gray-50 dark:bg-zinc-950 ${inter.className}`}>
        {children}
      </body>
    </html>
  )
}

