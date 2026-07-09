import React, { useEffect, useState } from 'react'
import api from '../api/axios'
import { useForm } from 'react-hook-form'

export default function ProfileEdit(){
  const { register, handleSubmit, setValue } = useForm()
  const [profile, setProfile] = useState<any>(null)

  useEffect(()=>{ fetchProfile() }, [])
  async function fetchProfile(){
    try{ const r = await api.get('/seeker/profile/') ; setProfile(r.data) ; setValue('headline', r.data.headline) ; setValue('summary', r.data.summary)}catch(e){ }
  }

  async function onSubmit(data:any){
    try{
      await api.patch('/auth/profile/', data)
      alert('Profile updated')
    }catch(e){ alert('Failed') }
  }

  return (
    <div className="app-shell p-4 max-w-2xl">
      <h2 className="text-xl mb-4">Edit Profile</h2>
      <form onSubmit={handleSubmit(onSubmit)} aria-label="Edit profile form">
        <label className="block mb-2">Headline
          <input {...register('headline')} className="w-full p-2 rounded mt-1" aria-required="false" />
        </label>
        <label className="block mb-2">Summary
          <textarea {...register('summary')} className="w-full p-2 rounded mt-1" rows={6} aria-required="false" />
        </label>
        <button type="submit" className="btn btn-primary">Save</button>
      </form>
    </div>
  )
}
