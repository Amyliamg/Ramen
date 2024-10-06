import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css/ramen.css';
import { FaShoppingCart } from 'react-icons/fa'; // shopping cart icon

function Ramen() {
    // store info
    const [soup, setSoup] = useState('');
    const [meat, setMeat] = useState('');
    const [spicy, setSpicy] = useState('');
    const [pendingOrderCount, setPendingOrderCount] = useState(0);
    const [currentSelection, setCurrentSelection] = useState('soup');  
    const navigate = useNavigate();

  
    // get the # of pending order when opens the page
    useEffect(() => {
        fetchPendingOrders();
    }, []);

    async function fetchPendingOrders() {
        try {
            const response = await fetch('http://127.0.0.1:8000/pending/orders');
            const data = response.ok ? await response.json() : [];
            setPendingOrderCount(data.length);
            // console.log('Pending Orders:', data.length);   
        } catch (error) {
            console.error('Error fetching pending orders:', error);
            setPendingOrderCount(0);
        }
    }

    function handleSelection(type, value) {
        if (type === 'soup') setSoup(value);
        else if (type === 'meat') setMeat(value);
        else if (type === 'spicy') setSpicy(value);
        setCurrentSelection(type);
    }

    async function submitRamenOrder(e) {
        const ramenData = { Soup: soup, Meat: meat, Spicy: spicy };

        try {
            const ramenResponse = await fetch('http://127.0.0.1:8000/ramen/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(ramenData),
            });

            if (ramenResponse.ok) {
                const { Ramen_id } = await ramenResponse.json();
                const orderResponse = await fetch('http://127.0.0.1:8000/order/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ Ramen_id }),
                });

                if (orderResponse.ok) {
                    alert(`Order for Ramen ID ${Ramen_id} has been placed!`);
                    fetchPendingOrders();   
                } else {
                    alert('Failed to place the order. Please try again.');
                }
            } else {
                alert('Failed to add ramen. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
        }
    }

    return (
        <div className="ramen-selection-container">
            <div className="header-container">
                <button className="button view-order-button" onClick={() => navigate('/order')}>
                    <div className="icon-container">
                        <FaShoppingCart />
                        {pendingOrderCount > 0 && <span className="order-count">+{pendingOrderCount}</span>}
                    </div>
                    <span className="button-text">View Order</span>
                </button>
                <h1>Design Your Ramen</h1>
            </div>
    
            <div className="selection-buttons">
                <div 
                    className={`selection-button ${currentSelection === 'soup' ? 'selected' : ''}`} 
                    onClick={() => handleSelection('soup', soup)}
                >
                    Soup
                </div>
                <div 
                    className={`selection-button ${currentSelection === 'meat' ? 'selected' : ''}`} 
                    onClick={() => handleSelection('meat', meat)}
                >
                    Meat
                </div>
                <div 
                    className={`selection-button ${currentSelection === 'spicy' ? 'selected' : ''}`} 
                    onClick={() => handleSelection('spicy', spicy)}
                >
                    Spicy
                </div>
            </div>
    
            <div className="options-container">
                {currentSelection === 'soup' && (
                    <>
                        <div 
                            className={`option ${soup === 'Miso' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('soup', 'Miso')}
                        >
                            <div className="emoji">🍜</div>
                            <div className="value">Miso</div>
                        </div>
                        <div 
                            className={`option ${soup === 'Shoyu' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('soup', 'Shoyu')}
                        >
                            <div className="emoji">🍲</div>
                            <div className="value">Shoyu</div>
                        </div>
                        <div 
                            className={`option ${soup === 'Tonkatso' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('soup', 'Tonkatso')}
                        >
                            <div className="emoji">🥢</div>
                            <div className="value">Tonkatso</div>
                        </div>
                    </>
                )}
                {currentSelection === 'meat' && (
                    <>
                        <div 
                            className={`option ${meat === 'Chicken' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('meat', 'Chicken')}
                        >
                            <div className="emoji">🍗</div>
                            <div className="value">Chicken</div>
                        </div>
                        <div 
                            className={`option ${meat === 'Pork' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('meat', 'Pork')}
                        >
                            <div className="emoji">🍖</div>
                            <div className="value">Pork</div>
                        </div>
                        <div 
                            className={`option ${meat === 'Tofu' ? 'selected' : ''}`} 
                            onClick={() => handleSelection('meat', 'Tofu')}
                        >
                            <div className="emoji">🌱</div>
                            <div className="value">Tofu</div>
                        </div>
                    </>
                )}
                {currentSelection === 'spicy' && (
                    <>
                        <div 
                            className={`option ${spicy === 0 ? 'selected' : ''}`} 
                            onClick={() => handleSelection('spicy', 0)}
                        >
                            <div className="emoji">🥬</div>
                            <div className="value">0</div>
                        </div>
                        <div 
                            className={`option ${spicy === 1 ? 'selected' : ''}`} 
                            onClick={() => handleSelection('spicy', 1)}
                        >
                            <div className="emoji">🌶️</div>
                            <div className="value">1</div>
                        </div>
                        <div 
                            className={`option ${spicy === 2 ? 'selected' : ''}`} 
                            onClick={() => handleSelection('spicy', 2)}
                        >
                            <div className="emoji">🌶️🌶️</div>
                            <div className="value">2</div>
                        </div>
                    </>
                )}
            </div>
    
            <button className="button add-ramen-button" onClick={submitRamenOrder}>
                Add Ramen
            </button>
        </div>
    );
    
}

export default Ramen;
