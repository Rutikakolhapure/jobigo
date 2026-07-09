import React, { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/axios'

export default function JobDetail(){
  const { id } = useParams()
  const [job, setJob] = React.useState<any|null>(null)
  useEffect(()=>{ if(id) fetch() }, [id])
  async function fetch(){
    try{
      const res = await api.get(`/company/jobs/${id}/`)
      setJob(res.data)
    }catch(e){ console.error(e) }
  }
  if(!job) return <div>Loading...</div>
  return (
    <div className="app-shell p-6">
      <h2 className="text-2xl">{job.title}</h2>
      <p className="text-sm text-muted-foreground">{job.company?.name}</p>
      <div className="mt-4 whitespace-pre-wrap">{job.description}</div>
    </div>
  )
}
