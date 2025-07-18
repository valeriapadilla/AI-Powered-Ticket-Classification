'use client'

import { Drawer, IconButton, useMediaQuery, Button } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { useTheme } from '@mui/material/styles'
import { useState, useEffect } from 'react'
import type { Ticket } from '@/data/mockTickets'

type TicketDrawerProps = {
  ticket: Ticket | null
  onClose: () => void
}

export default function TicketDrawer({ ticket, onClose }: TicketDrawerProps) {
  const isOpen = !!ticket
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  const [editableLevel, setEditableLevel] = useState('l1')
  const [editablePriority, setEditablePriority] = useState('low')
  const [editableEta, setEditableEta] = useState(0)

  useEffect(() => {
    if (ticket) {
      setEditableLevel(ticket.level)
      setEditablePriority(ticket.priority)
      setEditableEta(ticket.eta)
    }
  }, [ticket])

  const handleClose = () => {
    onClose()
  }

  const handleAccept = () => {
    console.log({
      level: editableLevel,
      priority: editablePriority,
      eta: editableEta,
    })
  }

  const isEditable = ticket?.status === 'pending'

  return (
    <Drawer
      anchor="right"
      open={isOpen}
      onClose={handleClose}
      variant={isMobile ? 'temporary' : 'persistent'}
      ModalProps={{
        keepMounted: false,
        disableEnforceFocus: true,
        disableAutoFocus: true,
      }}
      slotProps={{
        paper: {
          sx: {
            width: isMobile ? '100%' : '40vw',
            padding: '1.5rem',
            boxSizing: 'border-box',
            transition: 'transform 0.3s ease-in-out',
          },
          className: 'bg-background',
        },
      }}
    >
      {ticket && (
        <>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">{ticket.title}</h2>
            <IconButton onClick={handleClose}>
              <CloseIcon className="text-primary" />
            </IconButton>
          </div>
          <ul className="space-y-2 text-sm">
            <li>
              <strong>Status:</strong>{' '}
              {ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1)}
            </li>
            <li>
              <strong>Description:</strong> {ticket.description}
            </li>
            <li>
              <strong>Level:</strong>{' '}
              {isEditable ? (
                <select
                  className="border px-2 py-1 rounded w-full"
                  value={editableLevel}
                  onChange={(e) => setEditableLevel(e.target.value)}
                >
                  <option value="l1">L1</option>
                  <option value="l2">L2</option>
                  <option value="l3">L3</option>
                </select>
              ) : (
                ticket.level.toUpperCase()
              )}
            </li>
            <li>
              <strong>Priority:</strong>{' '}
              {isEditable ? (
                <select
                  className="border px-2 py-1 rounded w-full"
                  value={editablePriority}
                  onChange={(e) => setEditablePriority(e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              ) : (
                <span className={`text-priority-${ticket.priority}`}>
                  {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
                </span>
              )}
            </li>
            <li>
              <strong>ETA:</strong>{' '}
              {isEditable ? (
                <input
                  type="number"
                  className="border px-2 py-1 rounded w-full mb-4"
                  value={editableEta}
                  onChange={(e) => setEditableEta(Number(e.target.value))}
                  min={0}
                />
              ) : (
                ticket.eta
              )}
            </li>
          </ul>

          {isEditable && (
            <Button
              variant="contained"
              color="primary"
              onClick={handleAccept}
              className="w-full"
            >
              Aceptar
            </Button>
          )}
        </>
      )}
    </Drawer>
  )
}
