import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import api from '../api/axios'
import { useNavigate, useParams } from 'react-router-dom'

export default function JobEditor(){
  const { id } = useParams()
  const { register, handleSubmit, setValue } = useForm()
  const navigate = useNavigate()
  useEffect(()=>{ if(id) load() }, [id])
  async function load(){
    try{ const r = await api.get(`/company/jobs/${id}/`) ; Object.entries(r.data).forEach(([k,v])=> setValue(k as any, v)) }catch(e){ }
  }
  async function onSubmit(data:any){
    try{
      if(id) await api.patch(`/company/jobs/${id}/`, data)
      else await api.post('/company/jobs/', data)
      navigate('/dashboard')
    }catch(e){ alert('Failed to save') }
  }
  return (
    <div className="app-shell p-4 max-w-2xl mx-auto">
      <h2 className="text-xl mb-4">{id ? 'Edit Job' : 'Post Job'}</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <label className="block mb-2">Title<input {...register('title')} className="w-full p-2 rounded" /></label>
        <label className="block mb-2">Description<textarea {...register('description')} className="w-full p-2 rounded" rows={6} /></label>
        <label className="block mb-2">Employment Type<select {...register('employment_type')} className="w-full p-2 rounded"><option value="FULL_TIME">Full-time</option><option value="PART_TIME">Part-time</option></select></label>
        <button type="submit" className="btn btn-primary">Save</button>
      </form>
    </div>
  )
}
