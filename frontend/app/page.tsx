import TicketTabs from '@/components/TicketTabs'

export default function HomePage() {
  return (
    <main className="flex flex-col p-6 bg-background text-text justify-center items-center min-w-full w-full">
      <TicketTabs />
    </main>
  )
}
