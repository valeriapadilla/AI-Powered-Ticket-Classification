'use client'

import { useEffect, useState, useCallback } from 'react'
import TabHeader from './TabHeader'
import TicketList from './TicketList'
import TicketDrawer from './TicketDrawer'
import { Ticket } from '@/types/ticket'
import { fetchTickets } from '@/lib/api'
import { useMediaQuery } from '@mui/material'
import { useTheme } from '@mui/material/styles'

const tabs = ['Pending', 'In-progress', 'Resolved']

export default function TicketTabs() {
  const [activeTab, setActiveTab] = useState(0)
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)

  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  const loadTickets = useCallback(() => {
    fetchTickets()
      .then((data) => {
        console.log('Tickets updated:', data)
        setTickets(data)
      })
      .catch((error) => {
        console.error('Error fetching tickets:', error)
      })
  }, [])

  useEffect(() => {
    loadTickets()

    const interval = setInterval(() => {
      loadTickets()
    }, 10000)

    return () => clearInterval(interval)
  }, [loadTickets])

  const currentStatus = tabs[activeTab] as Ticket['status']
  const filteredTickets = tickets.filter(t => t.status === currentStatus)

  const handleUpdateTicket = () => {
    loadTickets()
    setSelectedTicket(null)
  }

  return (
    <div className="relative flex transition-all duration-300 w-full">
      <div
        className={`flex-1 transition-[margin] duration-300 ease-in-out ${
          !isMobile && selectedTicket ? 'mr-[40vw]' : 'mr-0'
        }`}
      >
        <h1 className="text-4xl font-bold mb-6 text-center">Tickets</h1>
        <TabHeader tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
        <TicketList tickets={filteredTickets} onSelect={setSelectedTicket} />
      </div>

      <TicketDrawer
        ticket={selectedTicket}
        onClose={() => setSelectedTicket(null)}
        onUpdate={handleUpdateTicket}
      />
    </div>
  )
}
