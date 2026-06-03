class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError(
                "Количество должно быть положительным"
            )
        self._quantity = value


    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"


    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"


    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        else:
            return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients


    def add_ingredient(self, ingredient):
        for product in self.ingredients:
            if product == ingredient:
                product.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)


    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError(
                "Неверный коэффициент(ratio). Требуется ввести положительное число"
            )
        new_ingredients = []
        for product in self.ingredients:
            new_ingredient = Ingredient(
                product.name,
                product.quantity * ratio,
                product.unit
            )
            new_ingredients.append(new_ingredient)
        return Recipe(self.title, new_ingredients)


    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        text = self.title + "\n"
        text += "Ингредиенты:\n"
        count = 1
        for ingredient in self.ingredients:
            text += str(count) + ")" + str(ingredient) + "\n"
            count += 1
        return text


class ShoppingList:
    def __init__(self):
        self._items = []


    def add_recipe(self, recipe, portions=1):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))


    def remove_recipe(self, title):
        new_items = []
        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                new_items.append((ingredient, recipe_title))
        self._items = new_items


    def get_list(self):
        totals = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in totals:
                totals[key] += ingredient.quantity
            else:
                totals[key] = ingredient.quantity
        result = []
        for key, quantity in totals.items():
            name, unit = key
            result.append(Ingredient(name, quantity, unit))
        result.sort(key=lambda ingredient: ingredient.name)
        return result


    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return False
        new_shopping_list = ShoppingList()
        for ingredient, recipe_title in self._items:
            new_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity,
                ingredient.unit
            )
            new_shopping_list._items.append((new_ingredient, recipe_title))
        for ingredient, recipe_title in other._items:
            new_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity,
                ingredient.unit
            )
            new_shopping_list._items.append((new_ingredient, recipe_title))
        return new_shopping_list


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type


    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(
            self.title,
            self.diet_type,
            scaled_recipe.ingredients
        )


    def __str__(self):
        return "[" + self.diet_type + "] " + super().__str__()