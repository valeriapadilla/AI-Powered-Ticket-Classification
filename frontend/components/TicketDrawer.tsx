'use client'

import { Drawer, IconButton, useMediaQuery, Button } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { useTheme } from '@mui/material/styles'
import { useState, useEffect } from 'react'
import { classifyTicket } from '@/lib/api'
import type { Ticket } from '@/types/ticket'

type TicketDrawerProps = {
  ticket: Ticket | null
  onClose: () => void
  onUpdate?: (updated: Ticket) => void
}

export default function TicketDrawer({ ticket, onClose, onUpdate }: TicketDrawerProps) {
  const isOpen = !!ticket
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  const [editableLevel, setEditableLevel] = useState('L1')
  const [editablePriority, setEditablePriority] = useState<'Low' | 'Medium' | 'High'>('Low')
  const [editableEta, setEditableEta] = useState<number>(0)

  useEffect(() => {
    if (ticket) {
      setEditableLevel(ticket.level)
      setEditablePriority(ticket.priority as 'Low' | 'Medium' | 'High')
      setEditableEta(ticket.eta ?? 0)
    }
  }, [ticket])

  const handleClose = () => {
    onClose()
  }

  const handleAccept = async () => {
    if (!ticket) return

    try {
      await classifyTicket(ticket.github_issue_id, {
        level: editableLevel,
        priority: editablePriority,
        eta: editableEta,
      })

      if (onUpdate) {
        onUpdate({
          ...ticket,
          level: editableLevel,
          priority: editablePriority,
          eta: editableEta,
        })
      }

      onClose()
    } catch (err) {
      alert('Error updating the ticket')
    }
  }

  const isEditable = ticket?.status === 'Pending'

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
              <strong>Status:</strong> {ticket.status}
            </li>
            <li>
              <strong>Description:</strong> {ticket.body || '—'}
            </li>
            <li>
              <strong>Level:</strong>{' '}
              {isEditable ? (
                <select
                  className="border px-2 py-1 rounded w-full"
                  value={editableLevel}
                  onChange={(e) => setEditableLevel(e.target.value)}
                >
                  <option value="L1">L1</option>
                  <option value="L2">L2</option>
                  <option value="L3">L3</option>
                </select>
              ) : (
                ticket.level ?? '—'
              )}
            </li>
            <li>
              <strong>Priority:</strong>{' '}
              {isEditable ? (
                <select
                  className="border px-2 py-1 rounded w-full"
                  value={editablePriority}
                  onChange={(e) =>
                    setEditablePriority(e.target.value as 'Low' | 'Medium' | 'High')
                  }
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                </select>
              ) : (
                <span className={`text-priority-${ticket.priority?.toLowerCase?.()}`}>
                  {ticket.priority ?? '—'}
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
                ticket.eta ?? '—'
              )}
            </li>
          </ul>

          {isEditable && (
            <Button
              variant="contained"
              color="primary"
              onClick={handleAccept}
              className="w-full mt-4"
            >
              Aceptar
            </Button>
          )}
        </>
      )}
    </Drawer>
  )
}
