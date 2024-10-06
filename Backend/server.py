# server.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
import asyncio
from repository import (
    add_order_to_db, get_order_by_id, 
    get_pending_orders_from_db, 
    update_order_status,
    update_inventory,
    add_ramen_to_db,
    get_ramen_from_db
)
from models import Order, OrderCreate,Ramen, RamenCreate
from typing import List
import random


router = APIRouter()
machine_states = [False, False]  # Two machines, initially idleß

@router.get("/")
async def read_root():
    return "Type docs"

@router.post("/ramen/", response_model=Ramen)
async def add_ramen(ramen: RamenCreate):
    return await add_ramen_to_db(ramen)

@router.get("/ramen/{ramen_id}", response_model=Ramen)
async def get_ramen(ramen_id: int):
    return await get_ramen_from_db(ramen_id)


@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    return await get_order_by_id(order_id)

@router.post("/order/", response_model=Order)
async def add_order(order: OrderCreate):
    order_id = await add_order_to_db(order)
    new_order = Order(
        Order_id=order_id,
        Ramen_id=order.Ramen_id,
        Price=12,
        Status="pending",
        Timestamp=datetime.now()
    )
    return new_order

async def process_order(order, machine_id):
    global machine_states
    machine_states[machine_id] = True
    processing_time = random.randint(10, 15)
    await asyncio.sleep(processing_time)
    await update_order_status(order.Order_id, "Completed")
    await update_inventory(order.Ramen_id)
    machine_states[machine_id] = False
    return order.Order_id

@router.post("/run_pending_orders/")
async def run_pending_orders():
    pending_order_cache = await get_pending_orders_from_db()
    tasks = []
    while pending_order_cache:
        for machine_id in range(len(machine_states)):
            if not machine_states[machine_id] and pending_order_cache:
                order = pending_order_cache.pop(0)
                task = asyncio.create_task(process_order(order, machine_id))
                tasks.append(task)
        await asyncio.sleep(1)
    completed_order_ids = await asyncio.gather(*tasks)
    return {
        "status": "success" if completed_order_ids else "info",
        "completed_orders": completed_order_ids,
    }

@router.get("/pending/orders", response_model=List[Order])
async def get_pending_orders():
    return await get_pending_orders_from_db()
