from django.contrib import admin
from .models import Product, Recipe, RecipeProduct


class RecipeProductTabularInline(admin.TabularInline):
    model = RecipeProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'times_cooked')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ('name', )
    inlines = [RecipeProductTabularInline]
