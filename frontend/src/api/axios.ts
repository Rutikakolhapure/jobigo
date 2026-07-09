import axios from 'axios'
import store from '../store'
import { refreshToken, setCredentials, logout } from '../store/slices/authSlice'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' }
})

let isRefreshing = false
let failedQueue: any[] = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.request.use((config) => {
  const state = store.getState()
  const token = state.auth.access
  if (token) config.headers = { ...(config.headers || {}), Authorization: `Bearer ${token}` }
  return config
})

api.interceptors.response.use((res) => res, async (err) => {
  const originalRequest = err.config
  if (err.response && err.response.status === 401 && !originalRequest._retry) {
    if (isRefreshing) {
      return new Promise(function(resolve, reject) {
        failedQueue.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers['Authorization'] = 'Bearer ' + token
        return axios(originalRequest)
      }).catch((e) => Promise.reject(e))
    }

    originalRequest._retry = true
    isRefreshing = true
    try {
      const res = await store.dispatch(refreshToken())
      const newToken = (res as any).payload?.access
      if (newToken) {
        processQueue(null, newToken)
        originalRequest.headers['Authorization'] = 'Bearer ' + newToken
        return axios(originalRequest)
      }
    } catch (e) {
      processQueue(e, null)
      store.dispatch(logout())
      return Promise.reject(e)
    } finally {
      isRefreshing = false
    }
  }
  return Promise.reject(err)
})

export default api
