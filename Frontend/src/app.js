import React from 'react';
import { useNavigate } from 'react-router-dom';
import './css/app.css';  

function App() {
  const navigate = useNavigate();

  function startTap() {
    navigate('/ramen');  
  }

  // When the user clicks the page, navigate to /ramen
  return (
    <div className="container" onClick={startTap}>
      <h1 className="title">Hello!</h1>
      <h1 className="title">Tap to order</h1>
    </div>
  );
}

export default App;
