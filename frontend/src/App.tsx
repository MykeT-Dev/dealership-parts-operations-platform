import { useEffect, useState } from 'react'
import { Link, Route, Routes, useParams } from 'react-router-dom'
import './App.css'

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

function PartDetailPage() {
  const { id } = useParams()

  return (
    <div className="app">
      <h1 className="app__title">Part Detail Page</h1>
      <p className="app__status">Selected part ID: {id}</p>
    </div>
  )
}

function App() {
  const [data, setData] = useState<PartListResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const [submittedSearch, setSubmittedSearch] = useState('')
  const [offset, setOffset] = useState(0)

  async function fetchParts() {
    try {
      setIsLoading(true)
      setError(null)

      const params = new URLSearchParams()

      // Add the submitted search term only if the user searched for something
      if (submittedSearch.trim()) {
        params.append('search', submittedSearch.trim())
      }

      // Tell the backend which page of results we want
      params.append('offset', offset.toString())

      const url = `http://127.0.0.1:8000/parts?${params.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error('Failed to fetch parts.')
      }

      const result: PartListResponse = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setIsLoading(false)
    }
  }

  function handleSearchSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    // A new search should always start from page 1
    setOffset(0)
    setSubmittedSearch(searchInput)
  }

  useEffect(() => {
    fetchParts()
  }, [submittedSearch, offset])

  const limit = data?.limit ?? 25
  const currentPage = Math.floor(offset / limit) + 1
  const totalPages = data ? Math.ceil(data.total / limit) : 1

  const hasPreviousPage = offset > 0
  const hasNextPage = data ? offset + limit < data.total : false

  const startItemNumber = data && data.total > 0 ? offset + 1 : 0
  const endItemNumber = data ? offset + data.count : 0

  function handlePreviousPage() {
    setOffset((previousOffset) => Math.max(previousOffset - limit, 0))
  }

  function handleNextPage() {
    if (hasNextPage) {
      setOffset((previousOffset) => previousOffset + limit)
    }
  }

    return (
    <Routes>
      <Route
        path="/"
        element={
          <div className="app">
            <h1 className="app__title">Dealership Parts Portal</h1>
            <p className="app__subtitle">Frontend connected to FastAPI backend</p>

            <form onSubmit={handleSearchSubmit}>
              <input
                type="text"
                value={searchInput}
                onChange={(event) => setSearchInput(event.target.value)}
                placeholder="Search parts"
              />
              <button type="submit">Search</button>
            </form>

            {isLoading && <p className="app__status">Loading parts...</p>}
            {error && <p className="app__error">Error: {error}</p>}

            {data && (
              <div>
                {data.count > 0 ? (
                  <>
                    <p>
                      Showing {startItemNumber} to {endItemNumber} of {data.total} parts
                    </p>

                    <ul className="parts-list">
                      {data.items.map((part) => (
                        <li key={part.id} className="parts-list__item">
                          <Link to={`/parts/${part.id}`} className="parts-list__link">
                            <strong>{part.part_number}</strong> - {part.description}
                            <div className="parts-list__meta">
                              {part.public_price} - {part.stock_status}
                            </div>
                          </Link>
                        </li>
                      ))}
                    </ul>

                    {totalPages > 1 && (
                      <div className="pagination-controls">
                        <button onClick={handlePreviousPage} disabled={!hasPreviousPage}>
                          Previous
                        </button>

                        <span>
                          Page {currentPage} of {totalPages}
                        </span>

                        <button onClick={handleNextPage} disabled={!hasNextPage}>
                          Next
                        </button>
                      </div>
                    )}
                  </>
                ) : (
                  <p className="app__status">No parts found.</p>
                )}
              </div>
            )}
          </div>
        }
      />
      <Route path="/parts/:id" element={<PartDetailPage />} />
    </Routes>
  )
}

export default App