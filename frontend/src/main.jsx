import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './globals.css'
import App from './App.tsx'

// Remove loading screen when React mounts
const loadingScreen = document.getElementById('loading-screen');
if (loadingScreen) {
  loadingScreen.style.opacity = '0';
  loadingScreen.style.transition = 'opacity 0.5s ease-out';
  setTimeout(() => loadingScreen.remove(), 500);
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
