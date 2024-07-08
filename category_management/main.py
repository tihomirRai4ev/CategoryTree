from typing import Optional

from fastapi import FastAPI
from schemas import Similarity, Category
from similarity_service import similarity_service
from category_service import category_service
from category_tree_visualizer import category_tree_visualizer

app = FastAPI()


@app.post("/categories/")
def create_category(category: Category):
    return category_service.create_category(category)


@app.put("/categories/{name}")
def update_category(name: str, category: Category):
    return category_service.update_category(name, category)


@app.delete("/categories/{name}")
def delete_category(name: str):
    return category_service.delete_category(name)


@app.patch("/categories/{name}/move")
def move_category(name: str, new_parent_name: Optional[str] = None):
    return category_service.move_category(name, new_parent_name)


@app.get("/categories/{name}")
def get_category(name: str):
    return category_service.get_category(name)


@app.get("/categories/")
def get_categories(parent_name: Optional[str] = None):
    return category_service.get_categories(parent_name)


@app.get("/print_category_tree/{name}")
def visualize_category_tree(name: str):
    category = category_service.get_category(name)
    category_tree = category_tree_visualizer.build_category_tree(category)
    category_tree_visualizer.print_category_tree(category_tree)

    return {"detail": "Category tree printed to console"}


@app.post("/similarities/")
def create_similarity(similarity: Similarity):
    return similarity_service.create_similarity(similarity)


@app.delete("/similarities/")
def delete_similarity(similarity: Similarity):
    return similarity_service.delete_similarity(similarity)


@app.get("/similarities/{name}")
def get_similarities(name: str):
    return similarity_service.get_similarities(name)


# Rabbit Hole and Rabbit Island logic
@app.get("/rabbit_hole_and_islands/")
def rabbit_hole_and_islands():
    return category_service.find_longest_rabbit_hole_and_islands()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
