from hashlib import sha256 as hash
from time import time
from typing import List
from models.transaction import Transaction


class Block:
    def __init__(
        self, index: int, transactions: List[Transaction], prev_hash: str, timestamp
    ):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash

        self.name = "Genesis Block" if index == 0 else f"Block {index}"

        self.nonce = 0
        self.timestamp = timestamp
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.name}{self.timestamp}{self.transactions}{self.nonce}{self.prev_hash}"
        return hash(data.encode()).hexdigest()


# if __name__ == "__main__":
#     block = Block(0, "", [], 2)
#     print(block.__dict__)
#     for t in block.transactions:
#         print(t.__dict__)
