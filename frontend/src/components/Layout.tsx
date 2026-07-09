import React from 'react'
import { Link } from 'react-router-dom'
import { useAppSelector, useAppDispatch } from '../store/hooks'
import { logout } from '../store/slices/authSlice'

export default function Layout({ children }: { children: React.ReactNode }){
  const user = useAppSelector(s => s.auth.user)
  const dispatch = useAppDispatch()
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white/6 backdrop-blur-md p-4 shadow-sm">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link to='/' className="text-2xl font-bold">JobiGo</Link>
          <nav>
            <Link to='/jobs' className="mr-4">Jobs</Link>
            {user ? (
              <>
                <Link to='/dashboard' className="mr-4">Dashboard</Link>
                <button onClick={()=>dispatch(logout())} className="text-sm text-red-500">Logout</button>
              </>
            ) : (
              <Link to='/login'>Login</Link>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-6xl mx-auto p-6">{children}</main>
      <footer className="p-6 text-center text-sm text-muted-foreground">© JobiGo</footer>
    </div>
  )
}
