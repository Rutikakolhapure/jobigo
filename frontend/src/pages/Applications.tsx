import React, { useEffect, useState } from 'react'
import api from '../api/axios'

export default function Applications(){
  const [apps, setApps] = useState<any[]>([])
  useEffect(()=>{ fetchApps() }, [])
  async function fetchApps(){
    try{ const r = await api.get('/seeker/jobs/applications/') ; setApps(r.data) }catch(e){ }
  }
  return (
    <div className="app-shell p-4">
      <h2 className="text-xl mb-4">Your Applications</h2>
      <ul>
        {apps.map(a => (
          <li key={a.id} className="py-2 border-b">
            <div className="font-medium">{a.job_id}</div>
            <div className="text-sm text-muted-foreground">Applied at {new Date(a.applied_at).toLocaleString()} — {a.status}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
