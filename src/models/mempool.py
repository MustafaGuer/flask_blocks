from typing import List
from models.transaction import Transaction


class Mempool:
    def __init__(self):
        self.pending_transactions: List[Transaction] = []
        
    
