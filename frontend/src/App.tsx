import { useEffect, useState } from 'react';
import "./App.css";

type PartListItem = {
  id: string
  part_number: string
  description: string
  public_price: string
  stock_status: string
  category_name: string | null
  category_code: string | null
}

type PartListResponse = {
  limit: number
  offset: number
  count: number
  total: number
  items: PartListItem[]
}

function App() {
  const [data, setdata] = useState<PartListResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchParts() {
      try {
        const response = await fetch('http://127.0.0.1:8000/parts')

        if (!response.ok) {
          throw new Error(`Failed to fetch parts.`)
        }

        const result: PartListResponse = await response.json()
        setdata(result)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setIsLoading(false)
      }
    }

    fetchParts()
  }, [])

  return (
    <div className="app">
      <h1 className="app__title">Dealership Parts Portal</h1>
      <p className="app__subtitle">Frontend connected to FastAPI backend</p>

      {isLoading && <p className="app__status">Loading parts...</p>}
      {error && <p className="app__error">Error: {error}</p>}

      {data && (
        <div>
          <p>
            Showing {data.count} of {data.total} parts
          </p>

          <ul className="parts-list">
            {data.items.map((part) => (
              <li key={part.id} className="parts-list__item">
                <strong>{part.part_number}</strong> - {part.description}
                <div className="parts-list__meta">
                  {part.public_price} - {part.stock_status}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App