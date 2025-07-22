import TicketCard from './TicketCard'
import type { Ticket } from '@/types/ticket'

type TicketListProps = {
  tickets: Ticket[]
  onSelect: (ticket: Ticket) => void
}

export default function TicketList({ tickets, onSelect }: TicketListProps) {
  return (
    <div className="space-y-3">
      {tickets.map((t) => (
        <TicketCard key={t.github_issue_id} ticket={t} onClick={() => onSelect(t)} />
      ))}
    </div>
  )
}
