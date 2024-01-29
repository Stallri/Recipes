from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    times_cooked = models.PositiveIntegerField(default=0,
                                               verbose_name='Количество приготовленных блюд с этим продуктом')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    products = models.ManyToManyField('Product', through='RecipeProduct', related_name='recipes',
                                      verbose_name='Продукты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeProduct(models.Model):
    product = models.ForeignKey('Product', related_name='products_set', on_delete=models.CASCADE,
                                verbose_name='Продукт')
    recipe = models.ForeignKey('Recipe', related_name='recipes_set', on_delete=models.CASCADE, verbose_name='Рецепт')
    weight_grams = models.PositiveIntegerField(verbose_name='Вес в граммах')
