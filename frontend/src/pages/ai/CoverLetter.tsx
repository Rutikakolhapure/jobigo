import React from 'react'
import { useForm } from 'react-hook-form'
import api from '../../src/api/axios'

export default function CoverLetter(){
  const { register, handleSubmit } = useForm()
  const [result, setResult] = React.useState('')
  const onSubmit = async (data:any)=>{
    const res = await api.post('/ai/cover-letter/', data)
    setResult(res.data.cover_letter)
  }
  return (
    <div className="app-shell p-6">
      <h2>AI Cover Letter Generator</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <textarea {...register('resume_text')} placeholder="Paste resume text" className="w-full p-2 mb-2" />
        <textarea {...register('job_description')} placeholder="Paste job description" className="w-full p-2 mb-2" />
        <input {...register('skills')} placeholder="Comma separated skills" className="w-full p-2 mb-2" />
        <button type="submit" className="btn btn-primary">Generate</button>
      </form>
      {result && <div className="mt-4 p-4 bg-white/5"> <pre className="whitespace-pre-wrap">{result}</pre> </div>}
    </div>
  )
}
