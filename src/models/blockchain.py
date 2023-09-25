from typing import List
from models.block import Block
from models.transaction import Transaction


class Blockchain:
    def __init__(self) -> None:
        self.blocks: List[Block] = [
            Block(0, [Transaction(0, "Foo", "Bar", "50")], "0000000", 2)
        ]

    def add_block(self, block: Block):
        self.blocks.append(block)
