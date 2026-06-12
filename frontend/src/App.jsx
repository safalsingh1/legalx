import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import TopicDetail from './pages/TopicDetail'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/topic/:key" element={<TopicDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
