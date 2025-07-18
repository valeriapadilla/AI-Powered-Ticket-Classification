'use client'

import { useState } from 'react'
import TabHeader from '@/components/TabHeader'
import TicketList from '@/components/TicketList'
import TicketDrawer from '@/components/TicketDrawer'
import { Ticket, tickets } from '@/data/mockTickets'
import { useMediaQuery } from '@mui/material'
import { useTheme } from '@mui/material/styles'

const tabs = ['Pending', 'In-progress', 'Resolved']

export default function TicketTabs() {
  const [activeTab, setActiveTab] = useState(0)
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)

  const currentStatus = tabs[activeTab].toLowerCase() as Ticket['status']
  const filteredTickets = tickets.filter(ticket => ticket.status === currentStatus)

  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  return (
    <div className="relative flex transition-all duration-300 w-full">
      <div
        className={`
          flex-1
          transition-[margin] duration-300 ease-in-out
          ${!isMobile && selectedTicket ? 'mr-[40vw]' : 'mr-0'}
        `}
      >
        <h1 className="text-4xl font-bold mb-6 text-center">Tickets</h1>
        <TabHeader tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
        <TicketList tickets={filteredTickets} onSelect={setSelectedTicket} />
      </div>

      <TicketDrawer ticket={selectedTicket} onClose={() => setSelectedTicket(null)} />
    </div>
  )
}
