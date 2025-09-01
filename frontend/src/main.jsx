import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import 'semantic-ui-css/semantic.min.css'
import App from './pages/App'
import Login from './pages/Login'

function Root() {

    const token = localStorage.getItem('token')

    return (

        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/*" element={token ? <App /> : <Navigate to="/login" />} />
            </Routes>
        </BrowserRouter>
    )
}

createRoot(document.getElementById('root')).render(<Root />)

