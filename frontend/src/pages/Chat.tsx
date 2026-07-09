import React, { useEffect, useRef, useState } from 'react'
import { useAppSelector } from '../store/hooks'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../api/axios'
import ChatInput from '../components/ChatInput'
import { Bell, Check, Loader2 } from 'lucide-react'

export default function Chat(){
  const token = useAppSelector(s => s.auth.access)
  const [messages, setMessages] = useState<any[]>([])
  const [typingUsers, setTypingUsers] = useState<Record<string,boolean>>({})
  const wsRef = useRef<WebSocket|null>(null)
  const listRef = useRef<HTMLDivElement|null>(null)

  useEffect(()=>{
    if(!token) return
    const room = 'global' // demo room
    const url = `${(location.protocol==='https:'?'wss':'ws')}://${location.host}/ws/chat/${room}/`
    const ws = new WebSocket(url)
    ws.onopen = ()=>{
      console.log('ws open')
      // send auth header via first message if gateway strips headers in some environments
      ws.send(JSON.stringify({ type: 'auth', token }))
    }
    ws.onmessage = (ev)=>{
      const data = JSON.parse(ev.data)
      if(data.type === 'message') setMessages(m=>[...m, data.message])
      else if(data.type === 'typing') setTypingUsers(t => ({...t, [data.user_id]: data.is_typing}))
      else if(data.type === 'presence') setTypingUsers(t => ({...t, [data.user_id]: data.online}))
      else if(data.type === 'read') {
        setMessages(ms => ms.map(m => m.id === data.message_id ? {...m, is_read: true} : m))
      }
    }
    wsRef.current = ws
    return ()=>{ ws.close() }
  }, [token])

  useEffect(()=>{ // scroll to bottom on new messages
    if(listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight
  }, [messages])

  const send = (text: string)=>{
    const ws = wsRef.current
    if(ws && ws.readyState === WebSocket.OPEN){
      ws.send(JSON.stringify({ type: 'message.send', content: text, receiver_id: null }))
    }
  }

  const sendTyping = (isTyping:boolean)=>{
    const ws = wsRef.current
    if(ws && ws.readyState === WebSocket.OPEN){
      ws.send(JSON.stringify({ type: 'typing', is_typing: isTyping }))
    }
  }

  return (
    <div className="app-shell p-4 max-w-3xl mx-auto">
      <h2 className="text-xl mb-2">Chat</h2>
      <div ref={listRef} className="h-64 overflow-auto border p-2 mb-2 rounded">
        <AnimatePresence>
          {messages.map((m,i)=> (
            <motion.div key={m.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.18 }} className="py-1">
              <div className="flex items-start justify-between">
                <div>
                  <strong className="mr-2">{m.sender_id}</strong>
                  <span className="text-sm">{m.content}</span>
                </div>
                <div className="text-xs text-muted-foreground flex items-center gap-2">
                  {m.is_read ? <Check size={14} /> : <Loader2 size={14} />}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div className="mb-2" aria-live="polite">
        {Object.keys(typingUsers).filter(k=>typingUsers[k]).length > 0 && (
          <div className="text-sm text-muted-foreground flex items-center gap-2"><Bell size={14}/> Someone is typing...</div>
        )}
      </div>

      <ChatInput onSend={send} onTyping={sendTyping} />
    </div>
  )
}
