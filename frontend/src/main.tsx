import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path.js';
import '@shoelace-style/shoelace/dist/themes/dark.css'
import './index.css'
import App from './App.tsx'

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.0/cdn/');

// We apply dark theme class to html explicitly, although index.css also handles it optionally
document.documentElement.classList.add('sl-theme-dark');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
