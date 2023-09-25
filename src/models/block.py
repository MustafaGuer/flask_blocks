from hashlib import sha256 as hash
from time import time
from typing import List
from models.transaction import Transaction


class Block:
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        prev_hash: str,
        difficulty: int,
    ) -> None:
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash

        self.name = "Genesis Block" if index == 0 else f"Block {index}"

        self.time = time()
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        nonce = 0
        str_to_hash = (
            str(self.index)
            + str(self.transactions)
            + str(self.prev_hash)
            + str(self.time)
        )
        curr_hash = hash(str_to_hash.encode("utf-8")).hexdigest()
        while not curr_hash.startswith("0" * self.difficulty):
            curr_hash = hash((str_to_hash + str(nonce)).encode("utf-8")).hexdigest()
            nonce += 1
        return curr_hash


# if __name__ == "__main__":
#     block = Block(0, "", [], 2)
#     print(block.__dict__)
#     for t in block.transactions:
#         print(t.__dict__)
