import random
from string import ascii_letters, digits
from typing import List
from faker import Faker
from requests import Session
from schemas import Category, Similarity
import time

fake = Faker()
session = Session()
session.headers.update({'Content-Type': 'application/json'})

# TODO (traychev) read from config
BASE_URL = 'http://localhost:8080'


def generate_category_name():
    return ''.join(random.choice(ascii_letters + digits) for _ in range(10))


# Function to create random categories
def create_random_categories(num_categories: int) -> List[str]:
    category_names = []
    start_time = time.time()
    for _ in range(num_categories):
        category_name = generate_category_name()
        category_names.append(category_name)
        category = Category(name=category_name, description=fake.sentence(), image=fake.image_url(), parent_name=None)
        response = session.post(f"{BASE_URL}/categories/", json=category.dict())
        assert response.status_code == 200
    end_time = time.time()
    print(f"Created {num_categories} categories in {end_time - start_time:.4f} seconds.")
    return category_names


# Function to create random similarities
def create_random_similarities(category_names: List[str], num_similarities: int):
    start_time = time.time()
    for _ in range(num_similarities):
        category_name_1 = random.choice(category_names)
        category_name_2 = random.choice(category_names)
        similarity = Similarity(category_name_1=category_name_1, category_name_2=category_name_2)
        response = session.post(f"{BASE_URL}/similarities/", json=similarity.dict())
        assert response.status_code == 200
    end_time = time.time()
    print(f"Created {num_similarities} similarities in {end_time - start_time:.4f} seconds.")


# Function to test category retrieval speed
def test_category_retrieval(category_names: List[str]):
    start_time = time.time()
    for category_name in category_names:
        response = session.get(f"{BASE_URL}/categories/{category_name}")
        assert response.status_code == 200
    end_time = time.time()
    print(f"Retrieved {len(category_names)} categories in {end_time - start_time:.4f} seconds.")


def test_category_update(category_names: List[str]):
    start_time = time.time()
    for category_name in category_names:
        new_description = fake.sentence()
        updated_category = Category(name=category_name, description=new_description)
        response = session.put(f"{BASE_URL}/categories/{category_name}", json=updated_category.dict())
        assert response.status_code == 200
    end_time = time.time()
    print(f"Updated {len(category_names)} categories in {end_time - start_time:.4f} seconds.")


# Function to test category removal speed
def test_category_removal(category_names: List[str]):
    start_time = time.time()
    for category_name in category_names:
        response = session.delete(f"{BASE_URL}/categories/{category_name}")
        assert response.status_code == 200
    end_time = time.time()
    print(f"Deleted {len(category_names)} categories in {end_time - start_time:.4f} seconds.")


# Generate 200 random categories
print("Creating random categories...")
category_names = create_random_categories(2000)

# Generate 2000 random similarities
print("\nCreating random similarities...")
create_random_similarities(category_names, 20000)

# Test category retrieval speed
print("\nTesting category retrieval speed...")
test_category_retrieval(category_names)

# Test category update speed
print("\nTesting category update speed...")
test_category_update(category_names)

print("\nTest operations completed.")
