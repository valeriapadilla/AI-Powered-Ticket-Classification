import TicketCard from '@/components/TicketCard'
import type { Ticket } from '@/data/mockTickets'

type TicketListProps = {
  tickets: Ticket[]
  onSelect: (ticket: Ticket) => void
}

export default function TicketList({ tickets, onSelect }: TicketListProps) {
  return (
    <div className="space-y-3">
      {tickets.map((t) => (
        <TicketCard key={t.id} ticket={t} onClick={() => onSelect(t)} />
      ))}
    </div>
  )
}
