import React from 'react';
import { createRoot } from 'react-dom/client';
import { loadBrandFonts } from '../src/brand/fonts';
import { App } from './App';
import './styles.css';

loadBrandFonts();
createRoot(document.getElementById('root')!).render(<App />);
