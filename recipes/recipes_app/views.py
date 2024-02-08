from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import get_object_or_404
from itertools import chain
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .models import Recipe, Product, RecipeProduct


# При добавлении продукта в определенный рецепт и наличии этого продукта в рецепте, происходит увеличение веса продукта
# в граммах в данном рецепте. Если продукт не присутствует в данном рецепте, добавляет его.
def add_product_to_recipe(request, recipe_id, product_id, weight):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    product = get_object_or_404(Product, id=product_id)
    if RecipeProduct.objects.filter(recipe=recipe, product=product):
        with transaction.atomic():
            recipe_product = RecipeProduct.objects.select_for_update().get(recipe=recipe, product=product)
            recipe_product.weight_grams += weight
            recipe_product.save()
        return HttpResponse(f'{recipe}, {product}, {recipe_product.weight_grams} грамм(а)')
    recipe_product = RecipeProduct.objects.create(recipe=recipe, product=product, weight_grams=weight)
    return HttpResponse(f'{recipe}, {product}, {recipe_product.weight_grams} грамм(а)')


# Увеличение "количества приготовлений" каждого продукта, входящего в определенный рецепт, на 1
def cook_recipe(request, recipe_id):
    with transaction.atomic():
        products = Recipe.objects.select_for_update().get(id=recipe_id).products.all()
        products_response = {}
        for p in products:
            p.times_cooked += 1
            products_response[p.name] = p.times_cooked
        Product.objects.bulk_update(products, ['times_cooked'])
    return JsonResponse(products_response)


# Получение таблицы с рецептами блюд содержащих меньше 11 грамм определенного продукта, либо вовсе не содержащих его
def show_recipes_without_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recipes = list(chain(Recipe.objects.exclude(products=product), Recipe.objects.filter(
        products__products_set__weight_grams__lte=10, products=product)))

    return render(request, 'recipes_app/recipes_without_product.html',
                  context={'recipes': recipes})
