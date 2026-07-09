import React, { useEffect, useState } from 'react'

export default function DarkModeToggle(){
  const [dark, setDark] = useState<boolean>(false)
  useEffect(()=>{ if(localStorage.getItem('dark') === '1') { document.documentElement.classList.add('dark'); setDark(true) } }, [])
  function toggle(){
    const next = !dark
    setDark(next)
    if(next) document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')
    localStorage.setItem('dark', next? '1' : '0')
  }
  return (
    <button onClick={toggle} aria-pressed={dark} aria-label="Toggle dark mode" className="px-3 py-1 rounded">
      {dark ? '🌙 Dark' : '☀️ Light'}
    </button>
  )
}
