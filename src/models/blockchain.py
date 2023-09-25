from typing import List
from models.block import Block
from models.transaction import Transaction
from time import time

POW_DIFFICULTY = 2


class Blockchain:
    def __init__(self) -> None:
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [Transaction(0, "Foo", "Bar", "50")], "0", time())

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.prev_hash = self.get_last_block().calculate_hash()
        new_block.nonce = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block: Block):
        while not block.calculate_hash().startswith("0" * POW_DIFFICULTY):
            block.nonce += 1
        return block.nonce

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if curr_block.prev_hash != prev_block.calculate_hash():
                return False

            return True
