import React, { useEffect, useState } from 'react'
import api from '../api/axios'
import { motion } from 'framer-motion'

export default function RecruiterJobs(){
  const [jobs, setJobs] = useState<any[]>([])
  useEffect(()=>{ fetchJobs() }, [])
  async function fetchJobs(){
    try{ const r = await api.get('/company/companies/') /* replace with recruiter jobs endpoint when available */ ; setJobs([]) }catch(e){ }
  }

  async function togglePublish(job:any){
    try{
      // optimistic UI change
      const updated = { ...job, status: job.status === 'PUBLISHED' ? 'DRAFT' : 'PUBLISHED' }
      setJobs(js => js.map(j => j.id === job.id ? updated : j))
      // call API (placeholder)
      await api.post(`/company/jobs/${job.id}/publish/`, {})
    }catch(e){ console.error(e) }
  }

  return (
    <div className="app-shell p-4">
      <h2 className="text-xl mb-4">Your Jobs</h2>
      {jobs.length === 0 ? <p>No jobs yet</p> : (
        <div className="space-y-2">
          {jobs.map(j => (
            <motion.div key={j.id} layout initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-3 border rounded flex items-center justify-between">
              <div>
                <div className="font-medium">{j.title}</div>
                <div className="text-sm text-muted-foreground">{j.status} • {j.posted_at}</div>
              </div>
              <div className="flex gap-2">
                <button onClick={()=>togglePublish(j)} className="btn btn-outline">{j.status === 'PUBLISHED' ? 'Unpublish' : 'Publish'}</button>
                <a href={`/jobs/${j.id}`} className="text-indigo-500">View</a>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
