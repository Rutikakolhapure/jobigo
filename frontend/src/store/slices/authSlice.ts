import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from '../../src/api/axios'

interface AuthState {
  access: string | null
  refresh: string | null
  user: any | null
}

const initialState: AuthState = {
  access: localStorage.getItem('access') || null,
  refresh: localStorage.getItem('refresh') || null,
  user: JSON.parse(localStorage.getItem('user') || 'null')
}

export const login = createAsyncThunk('auth/login', async (payload: {email: string, password: string}) => {
  const res = await axios.post('/auth/token/', payload)
  return res.data
})

export const refreshToken = createAsyncThunk('auth/refresh', async (_, { getState }) => {
  const state: any = (getState() as any)
  const refresh = state.auth.refresh
  const res = await axios.post('/auth/token/refresh/', { refresh })
  return res.data
})

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state){
      state.access = null
      state.refresh = null
      state.user = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    },
    setCredentials(state, action){
      state.access = action.payload.access
      state.refresh = action.payload.refresh
      state.user = action.payload.user
      localStorage.setItem('access', action.payload.access)
      localStorage.setItem('refresh', action.payload.refresh)
      localStorage.setItem('user', JSON.stringify(action.payload.user))
    }
  },
  extraReducers: (builder) => {
    builder.addCase(login.fulfilled, (state, action) => {
      state.access = action.payload.access
      state.refresh = action.payload.refresh
      // token doesn't include user info; frontend should fetch profile separately
      localStorage.setItem('access', action.payload.access)
      localStorage.setItem('refresh', action.payload.refresh)
    })
    builder.addCase(refreshToken.fulfilled, (state, action) => {
      state.access = action.payload.access
      localStorage.setItem('access', action.payload.access)
    })
  }
})

export const { logout, setCredentials } = authSlice.actions
export default authSlice.reducer
