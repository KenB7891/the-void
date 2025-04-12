from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import connect_db, get_db, disconnect_db
from app.models import Message
from app.utils import sanitize_input
from sqlalchemy import func
from sqlalchemy.orm import Session

MAX_DISPLAYS = 10
MAX_YELL_MESSAGE_LENGTH = 1000

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    print('App is starting...')

    yield
    
    disconnect_db()
    print('App is shutting down')

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.post('/yell')
async def yell(request: Request, body: dict, db: Session = Depends(get_db)):
    user_agent = request.headers.get('User-Agent', '').lower()

    if 'curl' in user_agent:
        raise HTTPException(status_code=403, detail='Curl requests are not allowed.')    
       
    raw_message = body.get('message', '')
    if not raw_message.strip():
        raise HTTPException(status_code=400, detail='Nothing was added to The Void.')
    
    if len(raw_message) > MAX_YELL_MESSAGE_LENGTH:
        raise HTTPException(status_code=400, detail="Message is too long, even for The Void.")
    
    clean_message = sanitize_input(raw_message)
    if not clean_message:
        raise HTTPException(status_code=400, detail='Nothing was added to The Void.')

    final_msg = Message(content=clean_message, total_displays=0)
    db.add(final_msg)
    db.commit()

    return{'status': 'The Void has recieved your message!'}

@app.get('/peek')
async def peek(db: Session = Depends(get_db)):
    message = db.query(Message).order_by(func.random()).first()

    if not message:
        raise HTTPException(status_code=404, detail='The Void is empty.')

    if message.total_displays >= MAX_DISPLAYS:
        db.delete(message)
        db.commit()
    else:
        message.total_displays += 1
        db.commit()

    return {'message': message.content}