import { Ticket } from '@/types/ticket'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchTickets(): Promise<Ticket[]> {
  const res = await fetch(`${API_URL}/tickets/get-tickets`)
  if (!res.ok) throw new Error('Failed to fetch tickets')
  const raw = await res.json()
  return raw.map(adaptTicket)
}

function adaptTicket(raw: any): Ticket {
  return {
    github_issue_id: raw.github_issue_id,
    title: raw.title,
    body: raw.body,
    level: raw.level_label,
    priority: raw.priority_label,
    eta: raw.eta,
    status: raw.status,
  }
}

export async function classifyTicket(
  id: number,
  data: { level?: string; priority?: string; eta?: number }
) {
  const res = await fetch(`${API_URL}/tickets/classified/${id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!res.ok) throw new Error('Failed to update ticket')
  return res.json()
}
