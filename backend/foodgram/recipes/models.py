from django.db import models
from foodgram.validation import validate_under_zero
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Называние'
    )
    color = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.name}'


class Ingredient(models.Model):
    MEASUREMENT_UNITS = [
    ('г', 'Грамм'),
    ('кг', 'Килограмм'),
    ('Ст.л.', 'Столовая ложка'),
    ('мл', 'Миллилитр'),
    ('л', 'Литр'),
    ('шт', 'Штука'),
    ('по вкусу', 'По вкусу'),
    ('ч.л.', 'Чайная ложка'),
    ('капля', 'Капля'),
    ('горсть', 'Горсть'),
    ('стакан', 'Стакан'),
    ('кусок', 'Кусок'),
    ('банка', 'Банка'),
    ('щепотка', 'Щепотка'),
    ]
    name = models.CharField(
        max_length=20,
        verbose_name='Называние'
    )
    measurement_unit = models.CharField(
        max_length=20,
        choices=MEASUREMENT_UNITS,
        default='г',
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Называние'
        )
    pub_date = models.DateTimeField(
        'Дата Публикации',
        auto_now_add=True
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Quantity',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[validate_under_zero]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.name}'


class Quantity(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantity'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='quantity'
    )
    quantity = models.FloatField(
        verbose_name='Количество',
        validators=[validate_under_zero]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self) -> str:
        return f'{self.recipe} {self.ingredient} {self.quantity}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='fan'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='buyer'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppinglist'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
