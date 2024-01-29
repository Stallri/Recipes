from django.shortcuts import render
from django.http import HttpResponse, response
from django.shortcuts import get_object_or_404

from .models import Recipe, Product, RecipeProduct


# При добавлении продукта в определенный рецепт и наличии этого продукта в рецепте, происходит увеличение веса продукта
# в граммах в данном рецепте. Если продукт не присутствует в данном рецепте, добавляет его.
def add_product_to_recipe(request, recipe_id, product_id, weight):
    if request.method == 'GET':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        product = get_object_or_404(Product, id=product_id)
        if RecipeProduct.objects.filter(recipe=recipe, product=product):
            recipe_product = RecipeProduct.objects.get(recipe=recipe, product=product)
            recipe_product.weight_grams += weight
            recipe_product.save()
            return HttpResponse(f'{recipe}, {product}, {recipe_product.weight_grams} grams')

        recipe_product = RecipeProduct.objects.create(recipe=recipe, product=product, weight_grams=weight)
        return HttpResponse(f'{recipe}, {product}, {recipe_product.weight_grams} грамм(а)')


# Увеличение "количества приготовлений" каждого продукта, входящего в определенный рецепт, на 1
def cook_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    products = {}
    for product in recipe.products.all():
        product.times_cooked += 1
        product.save()
        products[product.name] = product.times_cooked
    return HttpResponse(products.items())


# Получение таблицы с рецептами блюд содержащих меньше 11 грамм определенного продукта, либо вовсе не содержащих его
def show_recipes_without_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recipes = []
    for recipe in Recipe.objects.all():
        if (product not in recipe.products.all() or
                product.products_set.filter(weight_grams__lte=10).filter(recipe=recipe)):
            recipes.append(recipe)

    return render(request, 'recipes_app/recipes_without_product.html',
                  context={'recipes': recipes})
