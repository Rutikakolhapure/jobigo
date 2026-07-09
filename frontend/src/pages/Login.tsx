import React from 'react'
import { useForm } from 'react-hook-form'
import { useAppDispatch } from '../store/hooks'
import { login, setCredentials } from '../store/slices/authSlice'
import api from './axios'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const { register, handleSubmit } = useForm()
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const onSubmit = async (data: any) => {
    try{
      const res = await dispatch(login(data)).unwrap()
      // Optionally fetch user profile
      const profile = await api.get('/auth/profile/')
      dispatch(setCredentials({ access: res.access, refresh: res.refresh, user: profile.data }))
      navigate('/dashboard')
    }catch(e){
      alert('Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 app-shell">
      <h2 className="text-2xl mb-4">Login</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-3">
          <input {...register('email')} placeholder="Email" className="w-full p-2 rounded" />
        </div>
        <div className="mb-3">
          <input {...register('password')} type="password" placeholder="Password" className="w-full p-2 rounded" />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
    </div>
  )
}
