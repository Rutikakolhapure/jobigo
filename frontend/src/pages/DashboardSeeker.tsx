import React, { useEffect, useState } from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function DashboardSeeker(){
  const [profile, setProfile] = useState<any>(null)
  const [saved, setSaved] = useState<any[]>([])

  useEffect(()=>{ fetchProfile() ; fetchSaved() }, [])
  async function fetchProfile(){
    try{ const r = await api.get('/seeker/profile/') ; setProfile(r.data) }catch(e){ }
  }
  async function fetchSaved(){
    try{ const r = await api.get('/seeker/jobs/saved/') ; setSaved(r.data) }catch(e){ }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <aside className="app-shell p-4">
        <h3 className="text-lg font-semibold">Profile</h3>
        {profile ? (
          <div>
            <p className="mt-2">{profile.headline}</p>
            <p className="text-sm text-muted-foreground">Completion: {profile.profile_completion}%</p>
            <Link to='/profile' className="text-indigo-500 mt-2 inline-block">Edit profile</Link>
          </div>
        ) : <p>Loading...</p>}
      </aside>

      <section className="md:col-span-2">
        <div className="app-shell p-4 mb-4">
          <h3 className="text-lg font-semibold">Saved Jobs</h3>
          {saved.length === 0 ? <p className="text-sm">No saved jobs yet.</p> : (
            <ul>
              {saved.map(s => (
                <li key={s.id} className="border-b py-2">
                  <Link to={`/jobs/${s.job_id}`} className="font-medium">View job</Link>
                  <div className="text-sm text-muted-foreground">Saved at {new Date(s.saved_at).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="app-shell p-4">
          <h3 className="text-lg font-semibold">Applications</h3>
          <Link to='/applications' className="text-indigo-500">View your applications</Link>
        </div>
      </section>
    </div>
  )
}
