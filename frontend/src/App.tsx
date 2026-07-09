import React, { Suspense, lazy } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './utils/ProtectedRoute'
import Layout from './components/Layout'

const Landing = lazy(() => import('./pages/Landing'))
const Login = lazy(() => import('./pages/Login'))
const Signup = lazy(() => import('./pages/Signup'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Jobs = lazy(() => import('./pages/Jobs'))
const JobDetail = lazy(() => import('./pages/JobDetail'))
const Chat = lazy(() => import('./pages/Chat'))
const CoverLetter = lazy(() => import('./pages/ai/CoverLetter'))

export default function App(){
  return (
    <Layout>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path='/' element={<Landing/>} />
          <Route path='/login' element={<Login/>} />
          <Route path='/signup' element={<Signup/>} />
          <Route path='/jobs' element={<Jobs/>} />
          <Route path='/jobs/:id' element={<JobDetail/>} />
          <Route path='/ai/cover-letter' element={<ProtectedRoute><CoverLetter/></ProtectedRoute>} />
          <Route path='/chat' element={<ProtectedRoute><Chat/></ProtectedRoute>} />
          <Route path='/dashboard' element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
          <Route path='*' element={<Navigate to='/' />} />
        </Routes>
      </Suspense>
    </Layout>
  )
}
