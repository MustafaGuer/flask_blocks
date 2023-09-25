from time import time


class Transaction:
    def __init__(self, id: int, sender: str, receiver: str, amount: str) -> None:
        
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

        self.time = time()
