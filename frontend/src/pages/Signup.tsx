import React from 'react'
import { useForm } from 'react-hook-form'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'

export default function Signup(){
  const { register, handleSubmit } = useForm()
  const navigate = useNavigate()

  const onSubmit = async (data: any) => {
    try{
      await api.post('/auth/register/', data)
      alert('Registered — check email for verification')
      navigate('/login')
    }catch(e){
      alert('Register failed')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 app-shell">
      <h2 className="text-2xl mb-4">Sign up</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input {...register('email')} placeholder="Email" className="w-full p-2 mb-2" />
        <input {...register('first_name')} placeholder="First name" className="w-full p-2 mb-2" />
        <input {...register('last_name')} placeholder="Last name" className="w-full p-2 mb-2" />
        <input {...register('password')} type="password" placeholder="Password" className="w-full p-2 mb-2" />
        <button type="submit" className="btn btn-primary">Sign up</button>
      </form>
    </div>
  )
}
