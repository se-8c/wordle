


from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    userId : str
    username: Optional[str] = None
    lastGameUTCTime: Optional[int] = 0
    WordleArray: Optional[list] = []
    # status = 1 default
    # status = 2 gaming
    # status = 3 finished but faild
    # status = 4 finished and success
    status: Optional[int] = 1
    word: Optional[str] = None

class charResult(BaseModel):
    # code = -2 means the letter is not in the word
    # code = -1 The word is in this letter but not in the correct position
    # code = 1 The word is in this letter and in the correct position
    letter : str
    code : int