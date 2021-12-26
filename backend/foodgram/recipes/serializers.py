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


class QuantityIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Quantity
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def get_name(self, obj):
        return obj.ingredient.name

    def get_id(self, obj):
        return obj.ingredient.id

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class QuantitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Quantity
        fields = ('id', 'amount')

    def get_id(self, obj):
        return obj.ingredient.id


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RetrieveRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = QuantityIngredientSerializer(many=True, source='amount')
    tags = TagSerializer(many=True)
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


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = QuantitySerializer(many=True, source='amount')
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
        for i in range(0, len(validated_data.get('amount'))):
            id = validated_data.get('amount')[i].get('id')
            amount = validated_data.get('amount')[i].get('amount')
            ingredient = Ingredient.objects.get(pk=id)
            Quantity.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
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
        for i in range(0, len(validated_data.get('amount'))):
            id = validated_data.get('amount')[i].get('id')
            amount = validated_data.get('amount')[i].get('amount')
            ingredient = Ingredient.objects.get(pk=id)
            Quantity.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount
            )
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = instance.id
        ingredients = []
        for i in range(0, len(ret['ingredients'])):
            amount = ret['ingredients'][i]['amount']
            quantity = Quantity.objects.get(recipe=instance, amount=amount)
            quantity_serializer = QuantityIngredientSerializer(quantity)
            ingredients.append(quantity_serializer.data)
        ret['ingredients'] = ingredients
        tags = []
        for i in ret['tags']:
            tag = Tag.objects.get(pk=i)
            tags_serializer = TagSerializer(tag)
            tags.append(tags_serializer.data)
        ret['tags'] = tags
        author = self.context.get('request').user
        author_serializer = CustomUserSerializer(
            author,
            context={'request': self.context.get('request')}
        )
        ret['author'] = author_serializer.data
        return ret


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
