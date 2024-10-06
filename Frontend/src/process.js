import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './css/process.css';  

const Process = () => {
    const [loading, setLoading] = useState(true);
    const [completedOrders, setCompletedOrders] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        runPendingOrders();
    }, []);

    function runPendingOrders() {
        async function fetchOrders() {
            try {
                const response = await fetch('http://127.0.0.1:8000/run_pending_orders/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.status === "success") {
                        setCompletedOrders(data.completed_orders);
                    } else {
                        alert(data.message || "No orders processed.");
                    }
                } else {
                    console.error('Error running orders:', response.statusText);
                    alert('Failed to process order. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing your order.');
            } finally {
                setLoading(false);  
            }
        }

        fetchOrders();
    }

    const handleBackToHome = () => {
        navigate('/');
    };

    return (
        <div className="order-page">
            {loading ? (
                <div className="loading-container">
                    <div className="ramen-animation">
                        🍜 <span>Ramen is on the way to you...</span>
                    </div>
                    <div className="loading-bar">
                        <div className="progress-bar"></div>
                    </div>
                </div>
            ) : (
                <div className="order-completed">
                    <h2>🎉 Order Completed!</h2>
                    <div className="thank-you-message">Thanks for your order!</div>
                    <p>Order IDs: {completedOrders.join(', ')}</p>
                    <button className="back-home-button" onClick={handleBackToHome}>Back to Home</button>
                </div>
            )}
        </div>
    );
};

export default Process;
