import React, { useEffect } from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function Jobs(){
  const [jobs, setJobs] = React.useState<any[]>([])
  useEffect(()=>{ fetchJobs() }, [])
  async function fetchJobs(){
    try{
      const res = await api.get('/company/jobs/')
      setJobs(res.data)
    }catch(e){ console.error(e) }
  }
  return (
    <div>
      <h2 className="text-2xl mb-4">Jobs</h2>
      <div className="grid grid-cols-1 gap-4">
        {jobs.map(j => (
          <div key={j.id} className="p-4 app-shell">
            <h3 className="text-lg font-semibold">{j.title}</h3>
            <p className="text-sm">{j.company?.name}</p>
            <Link to={`/jobs/${j.id}`} className="text-indigo-500">View</Link>
          </div>
        ))}
      </div>
    </div>
  )
}
