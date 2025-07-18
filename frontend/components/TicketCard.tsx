import type { Ticket } from '@/data/mockTickets'

type TicketCardProps = {
  ticket: Ticket
  onClick: () => void
}

export default function TicketCard({ ticket, onClick }: TicketCardProps) {
  const priorityColorMap: Record<Ticket['priority'], string> = {
    high: 'text-priority-high',
    medium: 'text-priority-medium',
    low: 'text-priority-low',
  }

  const priorityClass = priorityColorMap[ticket.priority]
  const priorityText =
    ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)

  return (
    <div
      className="p-4 border rounded cursor-pointer hover:shadow transition bg-background"
      onClick={onClick}
    >
      <h3 className="font-semibold">{ticket.title}</h3>
      <p className={`text-sm font-medium ${priorityClass}`}>
        {priorityText}
      </p>
    </div>
  )
}
