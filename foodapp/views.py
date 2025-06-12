import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Food
from .serializers import FoodSerializer

@api_view(['GET'])
def search_food(request):
    query = request.GET.get('q', '')

    # Normalize function: remove special characters and lowercase
    def normalize(text):
        return re.sub(r'[^a-z0-9]', '', text.lower())

    # Normalized input without spaces or special characters
    normalized_query = normalize(query)

    matching_foods = []
    for food in Food.objects.all():
        normalized_description = normalize(food.description)

        # Check if cleaned query exists in cleaned description
        if normalized_query in normalized_description:
            matching_foods.append(food)

    serializer = FoodSerializer(matching_foods, many=True)
    return Response(serializer.data)
