from fastapi import HTTPException
from schemas import Similarity
from models import db


class SimilarityService:

    def __init__(self, in_memory_db):
        self.in_memory_db = in_memory_db
        self.categories = in_memory_db.categories
        self.category_tree = in_memory_db.category_tree
        self.similarities = in_memory_db.similarities

    def create_similarity(self, similarity: Similarity):
        category_name_1, category_name_2 = similarity.category_name_1, similarity.category_name_2
        if category_name_1 not in self.categories or category_name_2 not in self.categories:
            raise HTTPException(status_code=404, detail="One or both categories not found")

        self.similarities.add((category_name_1, category_name_2))
        self.similarities.add((category_name_2, category_name_1))
        return {"ok": True}

    '''
    By design if we try to delete non existing similarity - we don't throw exception but rather ignore
    '''
    def delete_similarity(self, similarity: Similarity):
        category_name_1, category_name_2 = similarity.category_name_1, similarity.category_name_2
        self.similarities.discard((category_name_1, category_name_2))
        self.similarities.discard((category_name_2, category_name_1))
        return {"ok": True}

    def get_similarities(self, name: str):
        if name not in self.categories:
            raise HTTPException(status_code=404, detail="Category not found")

        similar_categories = {cid2 for cid1, cid2 in self.similarities if cid1 == name}
        return [self.categories[cid] for cid in similar_categories]


similarity_service = SimilarityService(db)
