from fastapi import HTTPException
from typing import Optional
from schemas import Category
from models import db


class CategoryService:
    def __init__(self, in_memory_db):
        self.categories = in_memory_db.categories
        self.category_tree = in_memory_db.category_tree

    def create_category(self, category: Category):
        if category.parent_name:
            if category.parent_name not in self.categories:
                raise HTTPException(status_code=404, detail="Parent category not found")

            self.category_tree.setdefault(category.parent_name, []).append(category.name)
        else:
            self.category_tree[None].append(category.name)

        self.categories[category.name] = category
        return self.categories[category.name]

    def update_category(self, name: str, category_data: Category):
        if name not in self.categories:
            raise HTTPException(status_code=404, detail="Category not found")

        current_category = self.categories[name]
        updated_fields = category_data.dict(exclude_unset=True)

        for field, value in updated_fields.items():
            setattr(current_category, field, value)

        self.categories[name] = current_category
        return self.categories[name]

    def delete_category(self, name: str):
        if name not in self.categories:
            raise HTTPException(status_code=404, detail="Category not found")

        parent_name = self.categories[name].parent_name
        if parent_name in self.category_tree:
            self.category_tree[parent_name].remove(name)

        del self.categories[name]

        return {"message": f"Category '{name}' deleted successfully"}

    def move_category(self, name: str, new_parent_name: Optional[str]):
        if name not in self.categories:
            raise HTTPException(status_code=404, detail="Category not found")

        if new_parent_name is not None and new_parent_name not in self.categories:
            raise HTTPException(status_code=404, detail="New parent category not found")

        current_category = self.categories[name]
        current_parent_name = current_category.parent_name

        if current_parent_name in self.category_tree:
            self.category_tree[current_parent_name].remove(name)

        current_category.parent_name = new_parent_name

        if new_parent_name is None:
            self.category_tree[None].append(name)
        else:
            self.category_tree.setdefault(new_parent_name, []).append(name)

        return self.categories[name]

    def get_category(self, name: str):
        if name not in self.categories:
            raise HTTPException(status_code=404, detail="Category not found")
        return self.categories[name]

    def get_categories(self, parent_name: Optional[str] = None):
        if parent_name is not None and parent_name not in self.categories:
            raise HTTPException(status_code=404, detail="Parent category not found")

        return [self.categories[cid] for cid in self.category_tree.get(parent_name, [])]


category_service = CategoryService(db)
