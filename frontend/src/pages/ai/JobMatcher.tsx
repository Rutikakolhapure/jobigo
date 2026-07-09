import React, { useState } from 'react'
import api from '../../api/axios'

export default function JobMatcher(){
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [topK, setTopK] = useState(5)

  async function runMatch(){
    try{
      const res = await api.post('/ai/match-jobs/', { text: query, top_k: topK })
      setResults(res.data.results || [])
    }catch(e){ console.error(e) }
  }

  return (
    <div className="app-shell p-4 max-w-3xl">
      <h2 className="text-xl mb-4">AI Job Matcher</h2>
      <textarea value={query} onChange={e=>setQuery(e.target.value)} className="w-full p-2 mb-2" placeholder="Describe your skills or paste resume text" aria-label="Job matcher query" />
      <div className="flex items-center gap-2 mb-4">
        <label>Top K
          <input type="number" value={topK} onChange={e=>setTopK(Number(e.target.value))} min={1} max={50} className="ml-2 p-1 w-20" />
        </label>
        <button onClick={runMatch} className="btn btn-primary">Find matches</button>
      </div>
      <div>
        {results.map((r:any)=> (
          <div key={r.job.id} className="border-b p-2">
            <a href={`/jobs/${r.job.id}`} className="font-medium">{r.job.title}</a>
            <div className="text-sm text-muted-foreground">Score: {r.score.toFixed(3)}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
