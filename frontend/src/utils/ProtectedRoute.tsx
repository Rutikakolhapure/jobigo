import React from 'react'
import { useAppSelector } from '../store/hooks'
import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }: { children: React.ReactNode }){
  const token = useAppSelector(s => s.auth.access)
  if(!token){
    return <Navigate to='/login' />
  }
  return <>{children}</>
}
