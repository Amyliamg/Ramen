# repository.py
from db import get_db_connection
from models import OrderCreate, Order, RamenCreate,Ramen
from datetime import datetime
from fastapi import HTTPException

async def add_ramen_to_db(ramen: RamenCreate) -> Ramen:
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Determine Typeid based on Soup
        if ramen.Soup not in Ramen.Typeid:
            raise HTTPException(status_code=400, detail="Invalid Soup type provided.")
        
        type_id = Ramen.Typeid[ramen.Soup]

        cursor.execute('''
            INSERT INTO Ramen (Soup, Meat, Spicy, Typeid) VALUES (%s, %s, %s, %s);
        ''', (ramen.Soup, ramen.Meat, ramen.Spicy, type_id))
        connection.commit()
        ramen_id = cursor.lastrowid

        new_ramen = Ramen(
            Ramen_id=ramen_id,
            Soup=ramen.Soup,
            Meat=ramen.Meat,
            Spicy=ramen.Spicy,
            Typeid=type_id   
        )
        
        return new_ramen
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        connection.close()

async def get_ramen_from_db(ramen_id: int) -> Ramen:
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM Ramen WHERE Ramen_id = %s", (ramen_id,))
        ramen_data = cursor.fetchone()
        
        if ramen_data:
            # Dynamically determine Typeid based on the Soup
            soup = ramen_data[1]
            if soup not in Ramen.Typeid:
                raise HTTPException(status_code=400, detail="Invalid Soup type found in database.")
            
            type_id = Ramen.Typeid[soup]
            
            # Create Ramen instance and include Typeid
            ramen = Ramen(
                Ramen_id=ramen_data[0],
                Soup=ramen_data[1],
                Meat=ramen_data[2],
                Spicy=ramen_data[3],
                Typeid=type_id  # Include the Typeid here
            )
            return ramen
        else:
            raise HTTPException(status_code=404, detail="Ramen not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

async def get_order_by_id(order_id: int) -> Order:
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Orders WHERE Order_id = %s", (order_id,))
        order_data = cursor.fetchone()
        if order_data:
            return Order(
                Order_id=order_data[0],
                Ramen_id=order_data[1],
                Price=order_data[2],
                Status=order_data[3],
                Timestamp=order_data[4]
            )
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    finally:
        cursor.close()
        connection.close()

async def add_order_to_db(order: OrderCreate) -> int:
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Orders (Ramen_id, Price, Status, Timestamp) 
            VALUES (%s, %s, %s, %s)
        ''', (order.Ramen_id, 12, "pending", datetime.now()))
        connection.commit()
        return cursor.lastrowid  # Return the last inserted order ID
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database issue: " + str(e))
    finally:
        cursor.close()
        connection.close()

async def get_pending_orders_from_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Orders WHERE Status = %s", ('Pending',))
        pending_orders = cursor.fetchall()
        return [
            Order(
                Order_id=int(order[0]),
                Ramen_id=int(order[1]),
                Price=float(order[2]),
                Status=order[3],
                Timestamp=order[4]
            ) for order in pending_orders
        ] if pending_orders else []
    finally:
        cursor.close()
        connection.close()

async def update_order_status(order_id: int, new_status: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            UPDATE Orders
            SET Status = %s
            WHERE Order_id = %s
        ''', (new_status, order_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

async def update_inventory(ramen_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            UPDATE Inventory
            SET Quantity = Quantity - 1
            WHERE Ramen_Type_id = (SELECT Typeid FROM Ramen WHERE Ramen_id = %s)
        ''', (ramen_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
