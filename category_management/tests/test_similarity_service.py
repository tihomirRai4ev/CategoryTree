import sys

sys.path.append('..')

import pytest
from fastapi import HTTPException
from category_management.similarity_service import SimilarityService
from category_management.schemas import Similarity, Category
from category_management.models import InMemoryDatabase


@pytest.fixture
def db():
    return InMemoryDatabase()


@pytest.fixture
def similarity_service(db):
    return SimilarityService(db)


@pytest.fixture
def populate_categories(db):
    categories = [
        Category(name="root"),
        Category(name="child1", parent_name="root"),
        Category(name="child2", parent_name="root"),
        Category(name="child1_1", parent_name="child1"),
        Category(name="child1_2", parent_name="child1"),
        Category(name="child2_1", parent_name="child2"),
        Category(name="child2_2", parent_name="child2"),
        Category(name="child1_1_1", parent_name="child1_1"),
        Category(name="child1_1_2", parent_name="child1_1"),
        Category(name="child2_1_1", parent_name="child2_1"),
        Category(name="category3", parent_name="root"),
        Category(name="category4", parent_name="category3"),
        Category(name="category5", parent_name="category3"),
        Category(name="category6", parent_name="category3"),
        Category(name="category7", parent_name="category3"),
        Category(name="category8", parent_name="category3"),
        Category(name="category9", parent_name="category3"),
        Category(name="category10", parent_name="category3"),
        Category(name="category11", parent_name="category3"),
        Category(name="category12", parent_name="category3"),
        Category(name="category13", parent_name="category3"),
        Category(name="category14", parent_name="category3"),
        Category(name="category15", parent_name="category3"),
        Category(name="category16", parent_name="category3"),
        Category(name="category17", parent_name="category3"),
        Category(name="category18", parent_name="category3"),
        Category(name="category19", parent_name="category3"),
        Category(name="category20", parent_name="category3")
    ]
    for category in categories:
        db.categories[category.name] = category
        db.category_tree.setdefault(category.parent_name, []).append(category.name)


@pytest.fixture
def populate_similarities(db):
    similarities = [
        ("child1", "child2"),
        ("child2", "child1"),
        ("child1_1", "child1_2"),
        ("child1_2", "child1_1"),
        ("child2_1", "child2_2"),
        ("child2_2", "child2_1"),
        ("child1_1_1", "child1_1_2"),
        ("child1_1_2", "child1_1_1"),
        ("child2_1_1", "child2_1_1"),
        ("category3", "category4"),
        ("category4", "category5"),
        ("category5", "category6"),
        ("category6", "category7"),
        ("category7", "category8"),
        ("category8", "category9"),
        ("category9", "category10"),
        ("category10", "category11"),
        ("category11", "category12"),
        ("category12", "category13"),
        ("category13", "category14"),
        ("category14", "category15"),
        ("category15", "category16"),
        ("category16", "category17"),
        ("category17", "category18"),
        ("category18", "category19"),
        ("category19", "category20"),
        ("category20", "category3")
    ]
    for similarity in similarities:
        db.similarities.add(similarity)
        db.similarities.add((similarity[1], similarity[0]))


def test_create_multiple_similarities(similarity_service, populate_categories):
    similarities_to_create = [
        Similarity(category_name_1="child1_1", category_name_2="child1_2"),
        Similarity(category_name_1="child2_1", category_name_2="child2_2"),
        Similarity(category_name_1="category3", category_name_2="category4"),
        Similarity(category_name_1="category5", category_name_2="category6"),
        Similarity(category_name_1="category7", category_name_2="category8"),
        Similarity(category_name_1="category9", category_name_2="category10"),
        Similarity(category_name_1="category11", category_name_2="category12"),
        Similarity(category_name_1="category13", category_name_2="category14"),
        Similarity(category_name_1="category15", category_name_2="category16"),
        Similarity(category_name_1="category17", category_name_2="category18"),
        Similarity(category_name_1="category19", category_name_2="category20"),
    ]

    for similarity_data in similarities_to_create:
        response = similarity_service.create_similarity(similarity_data)
        assert response == {"ok": True}

    expected_similarities = [
        ("child1_1", "child1_2"),
        ("child1_2", "child1_1"),
        ("child2_1", "child2_2"),
        ("child2_2", "child2_1"),
        ("category3", "category4"),
        ("category4", "category3"),
        ("category5", "category6"),
        ("category6", "category5"),
        ("category7", "category8"),
        ("category8", "category7"),
        ("category9", "category10"),
        ("category10", "category9"),
        ("category11", "category12"),
        ("category12", "category11"),
        ("category13", "category14"),
        ("category14", "category13"),
        ("category15", "category16"),
        ("category16", "category15"),
        ("category17", "category18"),
        ("category18", "category17"),
        ("category19", "category20"),
        ("category20", "category19"),
    ]

    for similarity_pair in expected_similarities:
        assert similarity_pair in similarity_service.similarities


def test_get_similarities_large_dataset_add_inverted_similarity_succeeds(similarity_service, populate_categories,
                                                                         populate_similarities):
    similarities_to_create = [
        Similarity(category_name_1="category3", category_name_2="category4"),
        Similarity(category_name_1="category8", category_name_2="category3"),
        Similarity(category_name_1="category5", category_name_2="category6"),
    ]

    for similarity_data in similarities_to_create:
        response = similarity_service.create_similarity(similarity_data)
        assert response == {"ok": True}

    result = similarity_service.get_similarities("category3")

    assert len(result) == 3
    expected_names = ["category20", "category4", "category8"]

    for category in result:
        assert category.name in expected_names


def test_delete_similarities_large_dataset_succeeds(similarity_service, populate_categories, populate_similarities):
    response = similarity_service.delete_similarity(
        Similarity(category_name_1="category20", category_name_2="category3"))
    assert response == {"ok": True}

    response = similarity_service.delete_similarity(
        Similarity(category_name_1="category4", category_name_2="category3"))
    assert response == {"ok": True}

    result = similarity_service.get_similarities("category3")
    assert len(result) == 0


def test_delete_non_existent_similarity_not_throw(similarity_service, populate_categories, populate_similarities):
    response = similarity_service.delete_similarity(Similarity(category_name_1="A", category_name_2="B"))
    # By design, we don't throw exception but ignore
    assert response == {"ok": True}


def test_get_similarities_large_dataset_category_not_found(similarity_service, populate_categories):
    with pytest.raises(HTTPException) as exc_info:
        similarity_service.get_similarities("non_existing_category")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category not found"
