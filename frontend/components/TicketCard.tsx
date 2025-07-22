import type { Ticket } from '@/types/ticket'

type TicketCardProps = {
  ticket: Ticket
  onClick: () => void
}

export default function TicketCard({ ticket, onClick }: TicketCardProps) {
  const priorityColorMap: Record<Ticket['priority'], string> = {
    High: 'text-priority-high',
    Medium: 'text-priority-medium',
    Low: 'text-priority-low',
  }

  const priorityClass = priorityColorMap[ticket.priority]

  return (
    <div
      className="p-4 border rounded cursor-pointer hover:shadow transition bg-background"
      onClick={onClick}
    >
      <h3 className="font-semibold">{ticket.title}</h3>
      <p className={`text-sm font-medium ${priorityClass}`}>
        Priority: {ticket.priority}
      </p>
      <p className="text-sm">ETA: {ticket.eta ?? 'N/A'} days</p>
    </div>
  )
}
