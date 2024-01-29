from django.urls import path

from .views import add_product_to_recipe, cook_recipe, show_recipes_without_product


urlpatterns = [
    path('add-product-to-recipe/<int:recipe_id>/<int:product_id>/<int:weight>/', add_product_to_recipe),
    path('cook-recipe/<int:recipe_id>/', cook_recipe),
    path('show-recipes-without-product/<int:product_id>', show_recipes_without_product),
]
