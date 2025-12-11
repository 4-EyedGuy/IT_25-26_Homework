from fastapi import FastAPI, Depends, HTTPException, Query, Path
from typing import Annotated, Any
from .db import get_pool, close_pool
from .auth import get_user_by_token
from contextlib import asynccontextmanager
from pydantic import BaseModel
import hashlib
import secrets

from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib, secrets
from .db_orm import get_session
from .models import User, Token, Order, Good

pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await get_pool()
    yield
    pool = None
    await close_pool()

app = FastAPI(title="SQLi Lab (safe edition)", lifespan=lifespan)

class AuthRequest(BaseModel):
    name: str
    password: str

@app.post("/auth/token")
async def auth_token(body: AuthRequest, session: AsyncSession = Depends(get_session)):
    pass_hash = hashlib.md5(body.password.encode()).hexdigest()
    stmt = select(User).where(User.name == body.name, User.password_hash == pass_hash)
    user = (await session.execute(stmt)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stmt_token = select(Token).where(Token.user_id == user.id, Token.is_valid == True).limit(1)
    token_obj = (await session.execute(stmt_token)).scalar_one_or_none()
    
    if not token_obj:
        token_value = secrets.token_urlsafe(64)
        new_token = Token(user_id=user.id, value=token_value)
        session.add(new_token)
        await session.commit()
    else:
        token_value = token_obj.value

    return {"token": token_value}

@app.get("/orders")
async def list_orders(user: dict = Depends(get_user_by_token), limit: int = 10, offset: int = 0, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.user_id == user["id"]).order_by(Order.created_at.desc()).limit(limit).offset(offset)
    orders = (await session.execute(stmt)).scalars().all()
    return [{"id": o.id, "user_id": o.user_id, "created_at": o.created_at.isoformat()} for o in orders]

@app.get("/orders/{order_id}")
async def order_details(user: dict = Depends(get_user_by_token), order_id: int = Path(...), session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.id == order_id, Order.user_id == user["id"])
    order = (await session.execute(stmt)).scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    stmt_goods = select(Good).where(Good.order_id == order_id)
    goods = (await session.execute(stmt_goods)).scalars().all()
    
    return {
        "order": {"id": order.id, "user_id": order.user_id, "created_at": order.created_at.isoformat()},
        "goods": [{"id": g.id, "name": g.name, "count": g.count, "price": g.price} for g in goods]
    }