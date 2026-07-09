import React, { useState } from 'react'

export default function ChatInput({ onSend, onTyping }: { onSend: (t:string)=>void, onTyping?: (b:boolean)=>void }){
  const [val, setVal] = useState('')
  let typingTimer: any = null

  function handleChange(e:any){
    setVal(e.target.value)
    if(onTyping){
      onTyping(true)
      clearTimeout(typingTimer)
      typingTimer = setTimeout(()=> onTyping(false), 1200)
    }
  }

  function submit(){
    if(!val.trim()) return
    onSend(val.trim())
    setVal('')
    if(onTyping) onTyping(false)
  }

  return (
    <div className="flex gap-2">
      <input value={val} onChange={handleChange} className="flex-1 p-2 rounded" aria-label="Message input" />
      <button onClick={submit} className="btn btn-primary">Send</button>
    </div>
  )
}
