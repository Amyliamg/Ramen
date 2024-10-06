import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter , Route, Routes } from 'react-router-dom';
import App from './app';
import RamenPage from './ramen';
import OrderPage from './order';
import ProgressPage from './process';

const root = ReactDOM.createRoot(document.getElementById('root'));
// /           Homepage
// /ramen      Ramen Order Page
// /order      Order Page
// /process    Machine Making + finish window 


root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} /> 
      <Route path="/ramen" element={<RamenPage />} />
      <Route path="/order" element={<OrderPage />} />
      <Route path="/process" element={<ProgressPage />} />
    </Routes>
  </BrowserRouter>
);
