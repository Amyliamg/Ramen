import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css/cart.css'; 

const soupEmojis = {
    Shoyu: '🍜',   
    Miso: '🍲',    
    Tonkotsu: '🍥'
};

function Order() {
    const [ramenDetails, setRamenDetails] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchPendingOrders();  
    }, []);  

    
    function fetchPendingOrders() {
        async function fetchOrders() {
            try {
                const response = await fetch('http://127.0.0.1:8000/pending/orders', {
                    method: 'GET',
                    headers: {
                        'accept': 'application/json',
                    },
                });

                if (!response.ok) throw new Error(`Error: ${response.status}`);

                const orders = await response.json();

                const ramenResponses = await Promise.all(
                    orders.map(order =>
                        fetch(`http://127.0.0.1:8000/ramen/${order.Ramen_id}`, {
                            method: 'GET',
                            headers: {
                                'accept': 'application/json',
                            },
                        })
                    )
                );

                const ramenDetails = await Promise.all(
                    ramenResponses.map((response, index) => {
                        if (!response.ok) throw new Error(`Error: ${response.status}`);
                        return response.json().then(ramen => ({
                            Order_id: orders[index].Order_id,
                            Soup: ramen.Soup,
                            Meat: ramen.Meat,
                            Spicy: ramen.Spicy,
                        }));
                    })
                );

                setRamenDetails(ramenDetails);
            } catch (err) {
                console.error(`Error in fetching orders: ${err.message}`);
            }
        };

        fetchOrders();  
    }

    const totalPrice = ramenDetails.length * 12;  


    return (
        <div className="cart-container">
            <h1 className="order-title">Your Current Order</h1>
            {ramenDetails.length > 0 ? (
                <div className="receipt">
                    <ul style={{ listStyleType: 'none', padding: 0, display: 'flex', flexWrap: 'wrap' }}>
                        {ramenDetails.map(ramen => (
                            <li key={ramen.Order_id} className="ramen-item">
                                <p className="ramen-icon">{soupEmojis[ramen.Soup] || '🍜'}</p>
                                <p className="detail">Order ID: {ramen.Order_id}</p>
                                <p className="detail">Soup: {ramen.Soup}</p>
                                <p className="detail">Meat: {ramen.Meat}</p>
                                <p className="detail">Spicy Level: {ramen.Spicy}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>No pending orders in the cart.</p>
            )}
            <div className="total-price">
                <h2 className="price-title">Total Price: ${totalPrice.toFixed(2)}</h2>
            </div>
            <div className="cart-buttons">
                <button className="back-button" onClick={() => navigate('/ramen')}>
                    Back to Add Ramen
                </button>
                <button className="proceed-button" onClick={() => navigate('/process')}>
                    Order Now
                </button>
            </div>
        </div>
    );
}

export default Order;
