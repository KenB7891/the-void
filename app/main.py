from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from app.database import connect_db, get_db, disconnect_db
from app.models import Message
from app.utils import is_ip_allowed, sanitize_input, get_client_ip
from sqlalchemy import func
from sqlalchemy.orm import Session
import random
from datetime import datetime, timezone


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    print('App is starting...')

    yield
    
    disconnect_db()
    print('App is shutting down')

app = FastAPI(lifespan=lifespan)

@app.post('/yell')
async def yell(request: Request, body: dict):
    user_agent = request.headers.get('User-Agent', '').lower()

    if 'curl' in user_agent:
        raise HTTPException(status_code=403, detail='Curl requests are not allowed.')
    
    ip = get_client_ip(request)
    db: Session = next(get_db())

    if not is_ip_allowed(ip, db):
        raise HTTPException(status_code=429, detail='Yelling into The Void is on cooldown!')
    
    raw_message = body.get('message', '')
    if not raw_message.strip():
        raise HTTPException(status_code=400, detail='Nothing was added to The Void.')
    
    clean_message = sanitize_input(raw_message)
    if not clean_message:
        raise HTTPException(status_code=400, detail='Nothing was added to The Void.')

    final_msg = Message(content=clean_message, ip=ip, created_at=datetime.now(timezone.utc))
    db.add(final_msg)
    db.commit()

    return{'status': 'The Void has recieved your message!'}

@app.get('/peek')
async def peek(request: Request):
    db: Session = next(get_db())
    message = db.query(Message).order_by(func.random()).first()

    if not message:
        raise HTTPException(status_code=404, detail=f'The Void is empty')

    db.delete(message)
    db.commit()

    return {'message': message.content}