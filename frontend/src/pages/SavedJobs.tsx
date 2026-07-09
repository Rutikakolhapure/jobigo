import React, { useEffect, useState } from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function SavedJobs(){
  const [saved, setSaved] = useState<any[]>([])
  useEffect(()=>{ fetchSaved() }, [])
  async function fetchSaved(){
    try{ const r = await api.get('/seeker/jobs/saved/') ; setSaved(r.data) }catch(e){ }
  }
  return (
    <div className="app-shell p-4">
      <h2 className="text-xl mb-4">Saved Jobs</h2>
      <ul>
        {saved.map(s => (
          <li key={s.id} className="py-2 border-b">
            <Link to={`/jobs/${s.job_id}`} className="font-medium">View job</Link>
            <div className="text-sm text-muted-foreground">Saved at {new Date(s.saved_at).toLocaleString()}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
