# from django.shortcuts import render

# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Food
# from .serializers import FoodSerializer


# @api_view(['GET'])
# def search_food(request):
#     query = request.GET.get('q', '')
#     foods = Food.objects.filter(description__icontains=query)
#     serializer = FoodSerializer(foods, many=True)
#     return Response(serializer.data)



import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Food
from .serializers import FoodSerializer

@api_view(['GET'])
def search_food(request):
    query = request.GET.get('q', '').strip()

    def normalize(text):
        return re.sub(r'[^a-z0-9 ]', '', text.lower())

    normalized_query = normalize(query)
    query_words = normalized_query.split()

    matching_foods = []
    for food in Food.objects.all():
        normalized_description = normalize(food.description)

    
        if all(word in normalized_description for word in query_words):
            matching_foods.append(food)

    serializer = FoodSerializer(matching_foods, many=True)
    return Response(serializer.data)
