from pydantic import BaseModel
from typing import Optional, List


class Category(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    parent_name: Optional[str] = None
    children: List['Category'] = []


Category.update_forward_refs()


class Similarity(BaseModel):
    category_name_1: str
    category_name_2: str
