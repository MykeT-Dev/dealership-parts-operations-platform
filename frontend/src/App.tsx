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

type PartDetail = {
  id: string
  part_number: string
  description: string
  public_price: string
  stock_status: string
  category_name: string | null
  category_code: string | null
}

function formatPrice(price: string) {
  return `$${Number(price).toFixed(2)}`
}

function PartDetailPage() {
  const { id } = useParams()

  const [part, setPart] = useState<PartDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchPart() {
      try {
        setIsLoading(true)
        setError(null)

        const response = await fetch(`http://127.0.0.1:8000/parts/${id}`)

        if (!response.ok) {
          throw new Error('Failed to fetch part.')
        }

        const data = await response.json()
        setPart(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setIsLoading(false)
      }
    }

    if (id) {
      fetchPart()
    }
  }, [id])

  return (
    <div className="app">
      <div className="part-detail-layout">
        <div className="part-detail-header">
          <Link to="/" className="back-link">
            ← Back to Parts
          </Link>
          <h1 className="app__title">Part Detail</h1>
        </div>
    </div>

      {isLoading && (
        <div className="part-detail-card">
          <p className="app__status">Loading part details...</p>
        </div>
      )}

      {error && <p className="app__error">Error: {error}</p>}

      {part && (
  <div className="part-detail-card">
      <h2 className="part-detail-card__title">{part.part_number}</h2>
      <p className="part-detail-card__description">{part.description}</p>

      <div className="part-detail-card__meta">
        <p>
          <strong>Price:</strong> {formatPrice(part.public_price)}
        </p>
        <p>
          <strong>Status:</strong> {part.stock_status}
        </p>
        <p>
          <strong>Category:</strong> {part.category_name ?? 'N/A'}
        </p>
        <p>
          <strong>Category Code:</strong> {part.category_code ?? 'N/A'}
        </p>
      </div>
    </div>
  )}
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
  const [inStockOnly, setInStockOnly] = useState(false)

  async function fetchParts() {
    try {
      setIsLoading(true)
      setError(null)

      const params = new URLSearchParams()

      // Only include the in_stock when the toggle is on
      if (inStockOnly) {
        params.append('in_stock', 'true')
      }

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
  }, [submittedSearch, offset,inStockOnly])

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

              <label className="stock-toggle">
                <input
                  type="checkbox"
                  checked={inStockOnly}
                  onChange={(event) => {
                    setOffset(0)
                    setInStockOnly(event.target.checked)
                  }}
                />
                In Stock Only
              </label>
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
                              {formatPrice(part.public_price)} - {part.stock_status}
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