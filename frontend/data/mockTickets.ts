export type Ticket = {
  id: number
  title: string
  status: 'pending' | 'in-progress' | 'resolved'
  description: string
  level: 'l1' | 'l2' | 'l3'
  priority: 'high' | 'medium' | 'low'
  eta: number
}


export const tickets: Ticket[] = [
  {
    id: 1,
    title: 'Login bug',
    status: 'pending',
    description: 'Users receive error 500 on login.',
    level: 'l1',
    priority: 'high',
    eta: 2,
  },
  {
    id: 2,
    title: 'Dashboard update',
    status: 'in-progress',
    description: 'Updating layout and performance of dashboard.',
    level: 'l2',
    priority: 'medium',
    eta: 5,
  },
  {
    id: 3,
    title: 'Typo in footer',
    status: 'resolved',
    description: 'Fixed typo in footer copyright text.',
    level: 'l3',
    priority: 'low',
    eta: 1,
  },
  {
    id: 4,
    title: 'Email notifications failing',
    status: 'pending',
    description: 'Email service not sending alerts.',
    level: 'l1',
    priority: 'medium',
    eta: 3,
  },
]