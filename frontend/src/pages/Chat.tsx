import React, { useEffect, useRef, useState } from 'react'
import { useAppSelector } from '../store/hooks'

export default function Chat(){
  const token = useAppSelector(s => s.auth.access)
  const [messages, setMessages] = useState<any[]>([])
  const wsRef = useRef<WebSocket|null>(null)

  useEffect(()=>{
    if(!token) return
    const room = 'global' // demo room
    const url = `${(location.protocol==='https:'?'wss':'ws')}://${location.host}/ws/chat/${room}/?token=${token}`
    const ws = new WebSocket(url)
    ws.onopen = ()=>console.log('ws open')
    ws.onmessage = (ev)=>{
      const data = JSON.parse(ev.data)
      if(data.type === 'message') setMessages(m=>[...m, data.message])
    }
    wsRef.current = ws
    return ()=>{ ws.close() }
  }, [token])

  const send = (text: string)=>{
    const ws = wsRef.current
    if(ws && ws.readyState === WebSocket.OPEN){
      ws.send(JSON.stringify({ type: 'message.send', content: text, receiver_id: null }))
    }
  }

  return (
    <div className="app-shell p-4">
      <h2>Chat</h2>
      <div className="h-64 overflow-auto border p-2 mb-2">
        {messages.map((m,i)=> <div key={i}><strong>{m.sender_id}</strong>: {m.content}</div>)}
      </div>
      <ChatInput onSend={send} />
    </div>
  )
}

function ChatInput({ onSend }: { onSend: (text:string)=>void }){
  const [val, setVal] = useState('')
  return (
    <div className="flex gap-2">
      <input value={val} onChange={e=>setVal(e.target.value)} className="flex-1 p-2" />
      <button onClick={()=>{ onSend(val); setVal('') }} className="btn btn-primary">Send</button>
    </div>
  )
}
