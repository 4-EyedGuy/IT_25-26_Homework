# app/main.py

# Задача найти уязвимости SQL-инъекций и криптографические проблемы и исправить их.
# Я решил пойти по хардкорному пути и всё переписать на SQLAlchemy ORM с async-поддержкой.
# Команды очень противные (alembic мой любимый), но миграция прошла успешно.

# ORM автоматически параметризирует запросы, что защищает от SQL-инъекций, т.к. невозможно внедрить SQL-код через параметры.

# Также я добавил валидацию Pydantic для входных данных (path/query params).
# Она не позволит передать некорректные типы (например, строку вместо числа).

# Плюс выявились уязвимости в хэшировании паролей и токенов.
# MD5 легко взламывается, поэтому я его заменил на bcrypt и argon2.
# В базе хранятся bcrypt-хэши, а не открытые пароли или токены.

from fastapi import FastAPI, Depends, HTTPException, Path, Query
from .db import get_pool, close_pool
from contextlib import asynccontextmanager
from pydantic import BaseModel
import secrets
import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db_orm import get_session
from .models import User, Token, Order, Good
from .auth import get_user_by_token
from sqlalchemy import select


pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    try:
        yield
    finally:
        await close_pool()

app = FastAPI(title="SQLi Lab (safe edition)", lifespan=lifespan)

class AuthRequest(BaseModel):
    name: str
    password: str

@app.post("/auth/token")
async def auth_token(body: AuthRequest, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.name == body.name)
    user = (await session.execute(stmt)).scalars().one_or_none()
    
    if not user or not bcrypt.checkpw(body.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stmt_token = select(Token).where(Token.user_id == user.id, Token.is_valid == True).limit(1)
    token_obj = (await session.execute(stmt_token)).scalars().one_or_none()

    if not token_obj:
        token_value = secrets.token_urlsafe(64)
        token_hash = bcrypt.hashpw(token_value.encode(), bcrypt.gensalt()).decode()
        new_token = Token(user_id=user.id, value=token_hash)
        session.add(new_token)
        await session.commit()
    else:
        token_value = secrets.token_urlsafe(64)
        token_hash = bcrypt.hashpw(token_value.encode(), bcrypt.gensalt()).decode()
        token_obj.value = token_hash
        await session.commit()

    return {"token": token_value}

@app.get("/orders")
async def get_orders(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_user_by_token)
):

    stmt = (
        select(Order)
        .where(Order.user_id == current_user["id"])
        .offset(offset)
        .limit(limit)
    )

    orders = (await session.execute(stmt)).scalars().all()

    return [
        {
            "id": o.id,
            "created_at": o.created_at.isoformat(),
            "goods": [
                {"id": g.id, "name": g.name, "count": g.count, "price": g.price}
                for g in o.goods
            ]
        }
        for o in orders
    ]

@app.get("/orders/{order_id}")
async def get_order(
    order_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_user_by_token)
):

    stmt = select(Order).where(
        Order.id == order_id,
        Order.user_id == current_user["id"]
    )

    order = (await session.execute(stmt)).scalars().one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "created_at": order.created_at.isoformat(),
        "goods": [
            {"id": g.id, "name": g.name, "count": g.count, "price": g.price}
            for g in order.goods
        ]
    }