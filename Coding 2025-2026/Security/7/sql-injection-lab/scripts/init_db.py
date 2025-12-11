import asyncio
import sys
import secrets
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import bcrypt

from app.models import Base, User, Token, Order, Good

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async def init_db():
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        alice_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()
        bob_hash = bcrypt.hashpw(b"bobpass", bcrypt.gensalt()).decode()
        
        alice = User(
            name="alice",
            password_hash=alice_hash
        )
        bob = User(
            name="bob",
            password_hash=bob_hash
        )
        
        session.add(alice)
        session.add(bob)
        await session.flush()
        
        alice_token_value = "secrettokenAlice"
        bob_token_value = "secrettokenBob"
        
        alice_token = Token(
            value=bcrypt.hashpw(alice_token_value.encode(), bcrypt.gensalt()).decode(),
            is_valid=True,
            user_id=alice.id
        )
        bob_token = Token(
            value=bcrypt.hashpw(bob_token_value.encode(), bcrypt.gensalt()).decode(),
            is_valid=True,
            user_id=bob.id
        )
        
        session.add(alice_token)
        session.add(bob_token)
        await session.flush()
        
        order1 = Order(user_id=alice.id)
        order2 = Order(user_id=bob.id)
        
        session.add(order1)
        session.add(order2)
        await session.flush()
        
        good1 = Good(
            order_id=order1.id,
            name="Widget A",
            count=5,
            price=9.99
        )
        good2 = Good(
            order_id=order1.id,
            name="Widget B",
            count=3,
            price=15.50
        )
        good3 = Good(
            order_id=order2.id,
            name="Gadget X",
            count=2,
            price=29.99
        )
        
        session.add(good1)
        session.add(good2)
        session.add(good3)
        
        await session.commit()
    
    print("Database initialized successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
