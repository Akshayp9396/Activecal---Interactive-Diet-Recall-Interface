import csv
from django.core.management.base import BaseCommand
from foodapp.models import Food

class Command(BaseCommand):
    help = 'Load and merge food and nutrition CSV files'

    def handle(self, *args, **kwargs):
        # Load nutrition data into a dictionary
        nutrition_data = {}
        with open('foodapp/nutrition.csv', newline='', encoding='utf-8-sig') as nutrient_file:
            reader = csv.DictReader(nutrient_file)
            print(f"Nutrition CSV Headers: {reader.fieldnames}")

            for row in reader:
                # Clean headers and food code keys completely
                row = {key.replace('\ufeff', '').strip(): value for key, value in row.items() if key}

                food_code = row.get('Food code', '').strip()
                if not food_code.isdigit():
                    continue

                food_code = int(food_code)

                nutrition_data[food_code] = {
                    'calories': float(row.get('Energy (kcal)', 0) or 0),
                    'protein': float(row.get('Protein (g)', 0) or 0),
                    'fat': float(row.get('Total Fat (g)', 0) or 0),
                    'carbohydrates': float(row.get('Carbohydrate (g)', 0) or 0),
                }

        print(f"Loaded nutrition records: {len(nutrition_data)}")

        # Load food items and merge nutrition
        inserted_count = 0
        with open('foodapp/Food.csv', newline='', encoding='utf-8-sig') as food_file:
            reader = csv.DictReader(food_file)
            print(f"Food CSV Headers: {reader.fieldnames}")

            for row in reader:
                row = {key.replace('\ufeff', '').strip(): value for key, value in row.items() if key}

                food_code = row.get('Food code', '').strip()
                if not food_code.isdigit():
                    continue

                food_code = int(food_code)

                if food_code in nutrition_data:
                    Food.objects.create(
                        food_code=food_code,
                        description=row['Main food description'],
                        calories=nutrition_data[food_code]['calories'],
                        protein=nutrition_data[food_code]['protein'],
                        fat=nutrition_data[food_code]['fat'],
                        carbohydrates=nutrition_data[food_code]['carbohydrates'],
                    )
                    inserted_count += 1

        self.stdout.write(self.style.SUCCESS(f'{inserted_count} food records loaded successfully!'))

        if inserted_count == 0:
            self.stdout.write(self.style.WARNING('No records were loaded. Please double-check your CSV files and headers.'))
