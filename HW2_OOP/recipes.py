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
