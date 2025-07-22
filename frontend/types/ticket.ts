export interface Ticket {
  github_issue_id: number
  title: string
  body?: string
  level: string
  priority: 'High' | 'Medium' | 'Low'
  eta?: number
  status: 'Pending' | 'In-progress' | 'Resolved'
}
