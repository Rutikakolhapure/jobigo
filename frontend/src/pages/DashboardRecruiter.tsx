import React, { useEffect, useState } from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function DashboardRecruiter(){
  const [myJobs, setMyJobs] = useState<any[]>([])

  useEffect(()=>{ fetchMyJobs() }, [])
  async function fetchMyJobs(){
    try{ const r = await api.get('/company/companies/') ; /* placeholder for recruiter jobs API */ setMyJobs([]) }catch(e){ }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <aside className="app-shell p-4">
        <h3 className="text-lg font-semibold">Recruiter</h3>
        <Link to='/company/jobs/create' className="text-indigo-500 mt-2 inline-block">Post a job</Link>
      </aside>

      <section className="md:col-span-2">
        <div className="app-shell p-4">
          <h3 className="text-lg font-semibold">Your jobs</h3>
          {myJobs.length === 0 ? <p className="text-sm">No jobs posted yet.</p> : (
            <ul>
              {myJobs.map(j => (
                <li key={j.id} className="border-b py-2">
                  <Link to={`/jobs/${j.id}`} className="font-medium">{j.title}</Link>
                  <div className="text-sm text-muted-foreground">{j.status} • {j.posted_at}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </div>
  )
}
