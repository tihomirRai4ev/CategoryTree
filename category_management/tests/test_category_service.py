import sys

sys.path.append('..')

import pytest
from fastapi import HTTPException
from category_management.category_service import CategoryService
from category_management.models import InMemoryDatabase
from category_management.schemas import Category


@pytest.fixture
def db():
    return InMemoryDatabase()


@pytest.fixture
def category_service(db):
    return CategoryService(db)


def test_move_middle_node_to_root(category_service):
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
        Category(name="child2_1_1", parent_name="child2_1")
    ]

    for category in categories:
        category_service.create_category(category)

    # Move middle node 'child1_1' to one level above (root level)
    category_service.move_category(name="child1_1", new_parent_name="root")

    # Check the moved category
    moved_category = category_service.get_category(name="child1_1")
    assert moved_category.parent_name == "root"

    # Check the positions of other categories
    assert [cat.name for cat in category_service.get_categories(parent_name="root")] == ["child1", "child2", "child1_1"]
    assert [cat.name for cat in category_service.get_categories(parent_name="child1")] == ["child1_2"]
    assert [cat.name for cat in category_service.get_categories(parent_name="child2")] == ["child2_1", "child2_2"]
    assert [cat.name for cat in category_service.get_categories(parent_name="child2_1")] == ["child2_1_1"]

    # Check that the children of the moved category are not changed:
    assert [cat.name for cat in category_service.get_categories(parent_name="child1_1")] == ["child1_1_1", "child1_1_2"]

    # Ensure total number of categories remains the same (although we already checked this indirectly above)
    assert len(category_service.categories) == 10


def test_create_and_move_leaf_to_middle_node(category_service):
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
        Category(name="child2_1_1", parent_name="child2_1")
    ]

    for category in categories:
        category_service.create_category(category)

    initial_count = len(category_service.categories)
    category_service.move_category(name="child1_1_2", new_parent_name="child2_1")

    moved_category = category_service.get_category(name="child1_1_2")
    assert moved_category.parent_name == "child2_1"
    assert "child1_1_2" in [cat.name for cat in category_service.get_categories(parent_name="child2_1")]
    assert len(category_service.categories) == initial_count


def test_create_category_root(category_service):
    category = Category(name="root")
    created_category = category_service.create_category(category)
    assert created_category.name == "root"
    assert created_category.parent_name is None
    assert created_category in category_service.get_categories()


def test_create_category_with_parent(category_service):
    root_category = Category(name="root")
    category_service.create_category(root_category)

    child_category = Category(name="child", parent_name="root")
    created_category = category_service.create_category(child_category)
    assert created_category.name == "child"
    assert created_category.parent_name == "root"
    assert created_category in category_service.get_categories("root")


def test_create_category_with_nonexistent_parent(category_service):
    category = Category(name="orphan", parent_name="nonexistent")
    with pytest.raises(HTTPException) as exc_info:
        category_service.create_category(category)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Parent category not found"


def test_update_category(category_service):
    category = Category(name="root", description="Original")
    category_service.create_category(category)

    updated_category = Category(name="newName", description="Updated")
    result = category_service.update_category("root", updated_category)
    assert result.name == "newName"
    assert result.description == "Updated"


def test_update_nonexistent_category(category_service):
    updated_category = Category(name="root", description="Updated")
    with pytest.raises(HTTPException) as exc_info:
        category_service.update_category("nonexistent", updated_category)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category not found"


def test_delete_category(category_service):
    category = Category(name="root")
    category_service.create_category(category)

    result = category_service.delete_category("root")
    assert result["message"] == "Category 'root' deleted successfully"
    with pytest.raises(HTTPException) as exc_info:
        category_service.get_category("root")
    assert exc_info.value.status_code == 404


def test_delete_nonexistent_category(category_service):
    with pytest.raises(HTTPException) as exc_info:
        category_service.delete_category("nonexistent")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category not found"


def test_move_category(category_service):
    root_category = Category(name="root")
    category_service.create_category(root_category)

    child_category = Category(name="child", parent_name="root")
    category_service.create_category(child_category)

    category_service.move_category("child", None)
    assert "child" in [cat.name for cat in category_service.get_categories(None)]
    assert "child" not in [cat.name for cat in category_service.get_categories("root")]


def test_move_category_to_nonexistent_parent(category_service):
    root_category = Category(name="root")
    category_service.create_category(root_category)

    child_category = Category(name="child", parent_name="root")
    category_service.create_category(child_category)

    with pytest.raises(HTTPException) as exc_info:
        category_service.move_category("child", "nonexistent")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "New parent category not found"


def test_get_category(category_service):
    category = Category(name="root")
    category_service.create_category(category)

    result = category_service.get_category("root")
    assert result.name == "root"


def test_get_nonexistent_category(category_service):
    with pytest.raises(HTTPException) as exc_info:
        category_service.get_category("nonexistent")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category not found"


def test_get_categories_with_parent(category_service):
    root_category = Category(name="root")
    category_service.create_category(root_category)

    child_category = Category(name="child", parent_name="root")
    category_service.create_category(child_category)

    result = category_service.get_categories("root")
    assert len(result) == 1
    assert result[0].name == "child"


def test_get_categories_without_parent(category_service):
    root_category = Category(name="root")
    category_service.create_category(root_category)

    result = category_service.get_categories()
    assert len(result) == 1
    assert result[0].name == "root"
