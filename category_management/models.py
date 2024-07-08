from typing import Dict, List, Optional, Set, Tuple
from schemas import Category


class InMemoryDatabase:
    def __init__(self):
        self.categories: Dict[str, Category] = {}
        self.category_tree: Dict[Optional[str], List[str]] = {None: []}
        self.similarities: Set[Tuple[str, str]] = set()


db = InMemoryDatabase()
