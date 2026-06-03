import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def find_ingredient(ingredients, name, unit):
    for ingredient in ingredients:
        if ingredient.name == name and ingredient.unit == unit:
            return ingredient
    return None


def make_pancakes():
    recipe = Recipe("Блины")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Молоко", 300, "мл"))
    return recipe


def make_pie():
    recipe = Recipe("Пирог")
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Сахар", 100, "г"))
    return recipe


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_equal_same_name_and_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 200, "г")
    assert ingredient1 == ingredient2


def test_ingredient_not_equal_different_name():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Сахар", 500, "г")
    assert ingredient1 != ingredient2


def test_ingredient_not_equal_different_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 500, "кг")
    assert ingredient1 != ingredient2


def test_ingredient_negative_quantity_raises_error():
    with pytest.raises(ValueError):
        Ingredient("Мука", -500, "г")


def test_recipe_creation():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Блины", [flour])
    assert recipe.title == "Блины"
    assert recipe.ingredients == [flour]


def test_recipe_creation_without_ingredients():
    recipe = Recipe("Блины")
    assert recipe.title == "Блины"
    assert recipe.ingredients == []


def test_recipe_add_new_ingredient():
    recipe = Recipe("Блины")
    flour = Ingredient("Мука", 500, "г")
    recipe.add_ingredient(flour)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[0].unit == "г"


def test_recipe_add_same_ingredient_sums_quantity():
    recipe = Recipe("Блины")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_is_valid_ratio():
    assert Recipe.is_valid_ratio(2) is True
    assert Recipe.is_valid_ratio(0) is False
    assert Recipe.is_valid_ratio(-1) is False
    assert Recipe.is_valid_ratio("2") is False


def test_recipe_scale_returns_new_recipe():
    recipe = make_pancakes()
    scaled_recipe = recipe.scale(2)
    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe


def test_recipe_scale_changes_quantities():
    recipe = make_pancakes()
    scaled_recipe = recipe.scale(2)
    flour = find_ingredient(scaled_recipe.ingredients, "Мука", "г")
    milk = find_ingredient(scaled_recipe.ingredients, "Молоко", "мл")
    assert flour.quantity == 1000.0
    assert milk.quantity == 600.0


def test_recipe_scale_does_not_change_original_recipe():
    recipe = make_pancakes()
    recipe.scale(2)
    flour = find_ingredient(recipe.ingredients, "Мука", "г")
    milk = find_ingredient(recipe.ingredients, "Молоко", "мл")
    assert flour.quantity == 500.0
    assert milk.quantity == 300.0


def test_recipe_scale_invalid_ratio_raises_error():
    recipe = make_pancakes()
    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len_returns_unique_ingredients_count():
    recipe = Recipe("Блины")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Молоко", 300, "мл"))
    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = make_pancakes()
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()
    flour = find_ingredient(result, "Мука", "г")
    milk = find_ingredient(result, "Молоко", "мл")
    assert flour.quantity == 1000.0
    assert milk.quantity == 600.0


def test_shopping_list_remove_missing_recipe_does_nothing():
    pancakes = make_pancakes()
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pancakes, 1)
    shopping_list.remove_recipe("Несуществующий рецепт")
    result = shopping_list.get_list()
    flour = find_ingredient(result, "Мука", "г")
    milk = find_ingredient(result, "Молоко", "мл")
    assert flour.quantity == 500.0
    assert milk.quantity == 300.0


def test_shopping_list_get_list_sums_sameingredients():
    pancakes = make_pancakes()
    pie = make_pie()
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pancakes, 1)
    shopping_list.add_recipe(pie, 1)
    result = shopping_list.get_list()
    flour = find_ingredient(result, "Мука", "г")
    assert flour.quantity == 700.0


def test_shopping_list_get_list_returns_sorted_list():
    pancakes = make_pancakes()
    pie = make_pie()
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pancakes, 1)
    shopping_list.add_recipe(pie, 1)
    result = shopping_list.get_list()
    names = []
    for ingredient in result:
        names.append(ingredient.name)
    assert names == sorted(names)


def test_shopping_list_add_combines_two_lists():
    pancakes = make_pancakes()
    pie = make_pie()
    shopping_list1 = ShoppingList()
    shopping_list1.add_recipe(pancakes, 1)
    shopping_list2 = ShoppingList()
    shopping_list2.add_recipe(pie, 1)
    combined_list = shopping_list1 + shopping_list2
    result = combined_list.get_list()
    flour = find_ingredient(result, "Мука", "г")
    milk = find_ingredient(result, "Молоко", "мл")
    sugar = find_ingredient(result, "Сахар", "г")
    assert flour.quantity == 700.0
    assert milk.quantity == 300.0
    assert sugar.quantity == 100.0


def test_shopping_list_add_does_not_change_original_lists():
    pancakes = make_pancakes()
    pie = make_pie()
    shopping_list1 = ShoppingList()
    shopping_list1.add_recipe(pancakes, 1)
    shopping_list2 = ShoppingList()
    shopping_list2.add_recipe(pie, 1)
    shopping_list1 + shopping_list2
    result1 = shopping_list1.get_list()
    result2 = shopping_list2.get_list()
    flour1 = find_ingredient(result1, "Мука", "г")
    flour2 = find_ingredient(result2, "Мука", "г")
    assert flour1.quantity == 500.0
    assert flour2.quantity == 200.0


def test_dietary_recipe_str_has_diet_type_prefix():
    recipe = DietaryRecipe("Блины", "веган")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    assert str(recipe).startswith("[веган] Блины")