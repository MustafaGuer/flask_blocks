from time import time
from datetime import datetime


class Transaction:
    def __init__(self, id: int, sender: str, receiver: str, amount: str) -> None:
        
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

        self.timestamp = time()
        self.datetime = datetime.now()
