from models import Category


class CategoryTreeVisualizer:
    @staticmethod
    def build_category_tree(category: Category) -> Category:
        category.children = [CategoryTreeVisualizer.build_category_tree(child) for child in category.children]
        return category

    @staticmethod
    def print_category_tree(category: Category, indent: int = 0):
        print(' ' * indent + f'Name: {category.name}, Description: {category.description}, Image: {category.image}')
        for child in category.children:
            CategoryTreeVisualizer.print_category_tree(child, indent + 4)


category_tree_visualizer = CategoryTreeVisualizer()