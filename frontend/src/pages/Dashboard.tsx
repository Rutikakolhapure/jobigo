import React from 'react'
import { useAppSelector } from '../store/hooks'

const DashboardSeeker = React.lazy(() => import('./DashboardSeeker'))
const DashboardRecruiter = React.lazy(() => import('./DashboardRecruiter'))

export default function Dashboard(){
  const user = useAppSelector(s => s.auth.user)
  const role = user?.role || 'SEEKER'
  return (
    <React.Suspense fallback={<div>Loading dashboard...</div>}>
      {role === 'RECRUITER' ? <DashboardRecruiter/> : <DashboardSeeker/>}
    </React.Suspense>
  )
}
