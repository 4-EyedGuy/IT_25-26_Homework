from fastapi import HTTPException, Header, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload  # Для eager loading связанных User объектов
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from .db_orm import get_session
from .models import Token, User

async def get_user_by_token(
    authorization: str | None = Header(None), 
    session: AsyncSession = Depends(get_session)
):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    
    token_value = authorization[7:]
    
    stmt = (
        select(Token)
        .where(Token.is_valid == True)
        .join(User)
        .options(selectinload(Token.user))
    )
    tokens = (await session.execute(stmt)).scalars().all()
    
    token_obj = None
    for token in tokens:
        try:
            if bcrypt.checkpw(token_value.encode(), token.value.encode()):
                token_obj = token
                break
        except ValueError:
            continue
    
    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = token_obj.user
    return {"id": user.id, "name": user.name}
