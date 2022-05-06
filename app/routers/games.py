import json
from typing import Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4
from app.routers import JWTHelper
from app.routers.RespHelper import resp_err, resp_ok, resp_ok_code


import time
import uuid
from datetime import datetime

from models.user import User
from utils import words
router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{word}")
async def start(word: str, token: Optional[str] = Header(None)):
    word = word.lower()
    if token is None:
        # new player and  new game
        uid = uuid.uuid4().hex
        data = User(userId=uid)
        data.WordleArray = []
        data.status = 1
    else:
        # old player
        a = JWTHelper.decode_jwt(token)

        data = User(**a)
    # check game status
    # if data.status == 1 maing first time playing
    # if data.status == 2 playing
    # if data.status == 3 finished but faild
    # if data.status == 4 finished and success
    if data.status == 1:
        data.lastGameUTCTime = (int)(datetime.now().timestamp())
        data.WordleArray.clear()
        data.status = 2
        data.word = words.getRandomWord()
        # game start

    if data.status == 2:
        # game continue
        if len(data.WordleArray) >=5: # game is finished should return an error
            return resp_err(-5, "game is finished")
        code,array = words.isCorrect(input=word, word=data.word)
        if code == 2: # The word is fully correct. game is finished
            data.WordleArray.append(array)
            data.lastGameUTCTime = (int)(datetime.now().timestamp())
            data.status = 4
            return resp_ok_code(2,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
        if code == 3: # The word is partially correct.
            if len(data.WordleArray) >= 4: # game is finished.
                data.WordleArray.append(array)
                data.lastGameUTCTime = (int)(datetime.now().timestamp())
                data.status = 3
                return resp_ok_code(3,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
            else:
                data.WordleArray.append(array)
                return resp_ok_code(1,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
        if code == -3: # -3 is meaning the lenght of input is not equal to 5
            return resp_err(-3, "input is not equal to 5")
        if code == -4: # -4 is meaning the input is not a word
            return resp_err(-4, "input is not a word")
    
    if data.status == 3 or data.status == 4: # game is finished need to start a new game
        if data.lastGameUTCTime < datetime.now() + datetime.timedelta(days=1): # still to wait for 1 day
            return resp_err(-6, "still need to wait for 24 hours")
        else:
            data.status = 2
            data.WordleArray.clear()
            data.lastGameUTCTime = (int)(datetime.now().timestamp())
            data.word = words.getRandomWord()
            code,array = words.isCorrect(input=word, word=data.word)
            if code == 2: # The word is fully correct. game is finished
                data.WordleArray.append(array)
                data.lastGameUTCTime = (int)(datetime.now().timestamp())
                data.status = 4
                return resp_ok_code(2,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
            if code == 3: # The word is partially correct. game is finished
                if len(data.WordleArray) >= 4: # game is finished.
                    data.WordleArray.append(array)
                    data.lastGameUTCTime = (int)(datetime.now().timestamp())
                    data.status = 3
                    return resp_ok_code(3,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
                else:
                    data.WordleArray.append(array)
                    return resp_ok_code(1,{"word":data.word,"data":data.dict(),"token":JWTHelper.encoded_jwt(data.dict())})
            if code == -3: # -3 is meaning the lenght of input is not equal to 5
                return resp_err(-3, "input is not equal to 5")
            if code == -4: # -4 is meaning the input is not a word
                return resp_err(-4, "input is not a word")
