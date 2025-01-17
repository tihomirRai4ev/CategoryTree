import sys

sys.path.append('..')

import pytest
from category_management.rabbit_hole_script import RabbitHoleScript
from category_management.category_service import CategoryService
from category_management.similarity_service import SimilarityService
from category_management.schemas import Category, Similarity
from category_management.models import InMemoryDatabase
import time


@pytest.fixture
def db():
    return InMemoryDatabase()


@pytest.fixture
def rabbit_hole_script(db):
    return RabbitHoleScript(db)


@pytest.fixture
def category_service(db):
    return CategoryService(db)


@pytest.fixture
def similarity_service(db):
    return SimilarityService(db)


def test_create_adjacency_list_optimized(category_service, similarity_service, rabbit_hole_script):
    init_simple_example(category_service, similarity_service)

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    expected_adjacency_list = {
        "A": {"B", "D"},
        "B": {"A", "C", "D"},
        "C": {"B"},
        "D": {"A", "B"}
    }
    assert adjacency_list == expected_adjacency_list


def test_bfs(category_service, similarity_service, rabbit_hole_script):
    init_simple_example(category_service, similarity_service)

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    length, path = rabbit_hole_script.bfs_deepest_paths("A", adjacency_list)

    assert length == 2

    expected_paths = [
        ["A", "B", "C"],
    ]

    assert path == expected_paths


def test_find_longest_rabbit_hole_optimized(category_service, similarity_service, rabbit_hole_script):
    init_simple_example(category_service, similarity_service)

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    longest_paths = rabbit_hole_script.find_longest_rabbit_hole_optimized(adjacency_list)

    expected_longest_path = [["A", "B", "C"], ["B", "C", "D"]]

    assert len(longest_paths) == 2, f"Expected exactly 2 longest path, but got {len(longest_paths)} paths"
    assert set(longest_paths[0]) == set(expected_longest_path[0]) or set(longest_paths[0]) == set(
        expected_longest_path[1])


def test_find_longest_rabbit_hole_using_degrees(category_service, similarity_service, rabbit_hole_script):
    init_simple_example(category_service, similarity_service)

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    longest_paths = rabbit_hole_script.find_longest_rabbit_hole_optimized(adjacency_list)

    expected_longest_path = [["A", "B", "C"], ["B", "C", "D"]]

    assert len(longest_paths) == 2, f"Expected exactly 2 longest path, but got {len(longest_paths)} paths"
    assert set(longest_paths[0]) == set(expected_longest_path[0]) or set(longest_paths[0]) == set(
        expected_longest_path[1])


def test_find_rabbit_islands_optimized(category_service, similarity_service, rabbit_hole_script):
    init_simple_example(category_service, similarity_service)

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    rabbit_islands = rabbit_hole_script.find_rabbit_islands_optimized(adjacency_list)

    expected_rabbit_islands = [["A", "B", "C", "D"]]

    sorted_rabbit_islands = [sorted(island) for island in rabbit_islands]
    sorted_expected_islands = [sorted(island) for island in expected_rabbit_islands]

    assert sorted_rabbit_islands == sorted_expected_islands, f"Expected {sorted_expected_islands}, but got {sorted_rabbit_islands}"


def test_find_longest_rabbit_hole_with_large_data(category_service, similarity_service, rabbit_hole_script):
    generate_long_path_example(category_service, similarity_service)

    start_time = time.time()

    adjacency_list = rabbit_hole_script.create_adjacency_list_optimized()
    longest_paths = rabbit_hole_script.find_longest_rabbit_hole_optimized(adjacency_list)

    end_time = time.time()
    print(f"Method took {end_time - start_time:.4f} seconds.")

    assert len(longest_paths) == 1, \
        f"Expected exactly 1 longest path, but got {len(longest_paths)} paths"


def init_simple_example(category_service, similarity_service):
    categories = [
        Category(name="root"),
        Category(name="A", parent_name="root"),
        Category(name="B", parent_name="root"),
        Category(name="C", parent_name="root"),
        Category(name="D", parent_name="root"),
    ]

    for category in categories:
        category_service.create_category(category)

    similarities = [
        Similarity(category_name_1="A", category_name_2="B"),
        Similarity(category_name_1="A", category_name_2="D"),
        Similarity(category_name_1="B", category_name_2="C"),
        Similarity(category_name_1="B", category_name_2="D"),
    ]

    for similarity in similarities:
        similarity_service.create_similarity(similarity)


def generate_long_path_example(category_service, similarity_service):
    categories = [Category(name=f"Category_{i}") for i in range(1, 10001)]

    similarities = [
        Similarity(category_name_1=f"Category_{i}", category_name_2=f"Category_{i + 1}") for i in range(1, 10000)
    ]

    for category in categories:
        category_service.create_category(category)

    for similarity in similarities:
        similarity_service.create_similarity(similarity)

    expected_longest_path = [f"Category_{i}" for i in range(1, 10001)]

    return categories, similarities, expected_longest_path
