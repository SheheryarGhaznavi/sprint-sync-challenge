import { createRoot } from 'react-dom/client'

function Root() {
  return (
    <div>
      <h1>Hello, React!</h1>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<Root />)

