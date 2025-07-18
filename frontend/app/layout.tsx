import '@/styles/globals.css'
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter'
import { CssBaseline, GlobalStyles } from '@mui/material'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Tickets',
  description: 'Ticket UI',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider options={{ enableCssLayer: true }}>
          <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
          <CssBaseline />
          {children}
        </AppRouterCacheProvider>
      </body>
    </html>
  )
}
