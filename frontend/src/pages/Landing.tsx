import React from 'react'
import { Link } from 'react-router-dom'

export default function Landing(){
  return (
    <div className="app-shell p-8">
      <h1 className="text-4xl font-bold mb-2">JobiGo</h1>
      <p className="mb-6">AI-powered microservices job portal</p>
      <div>
        <Link to='/jobs' className="mr-4">Browse Jobs</Link>
        <Link to='/signup'>Get started</Link>
      </div>
    </div>
  )
}
