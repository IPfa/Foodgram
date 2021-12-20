from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CustomUserSerializer

from .models import Favorite, Ingredient, Quantity, Recipe, ShoppingList, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('measurement_unit',)


class QuantitySerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = Quantity
        fields = ('ingredient', 'quantity')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = QuantitySerializer(many=True, source='quantity')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.get('tags')
        recipe = Recipe(
            author=self.context.get('request').user,
            name=validated_data.get('name'),
            text=validated_data.get('text'),
            cooking_time=validated_data.get('cooking_time'),
            image=validated_data.get('image'),
        )
        recipe.save()
        recipe.tags.set(tags)
        for i in range(0, len(validated_data.get('quantity'))):
            full_ingredient = validated_data.get('quantity')[i]
            quantity = full_ingredient.get('quantity')
            ingredient = Ingredient.objects.get(
                name=full_ingredient.get('ingredient').get('name')
            )
            Quantity.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        quantity = Quantity.objects.filter(recipe=instance)
        for i in range(0, len(quantity)):
            quantity[i].delete()
        instance.author = self.context.get('request').user
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.image = validated_data.get('image')
        instance.save()
        instance.tags.set(tags)
        for i in range(0, len(validated_data.get('quantity'))):
            full_ingredient = validated_data.get('quantity')[i]
            quantity = full_ingredient.get('quantity')
            ingredient = Ingredient.objects.get(
                name=full_ingredient.get('ingredient').get('name')
            )
            Quantity.objects.create(
                recipe=instance,
                ingredient=ingredient,
                quantity=quantity
            )
        return instance


class RetrieveRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = QuantitySerializer(many=True, source='quantity')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(user=request.user, recipe=obj)
        if favorite.exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        favorite = ShoppingList.objects.filter(user=request.user, recipe=obj)
        if favorite.exists():
            return True
        return False


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
        recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        serializer = RetrieveRecipeSerializer(
            recipes,
            context={'request': request},
            many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
