from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Contoh data produk makanan sehat
foods = [
    {"id": "1", "name": "Salad Buah", "description": "Salad segar dengan buah-buahan pilihan", "price": 30000, "created_at": datetime.now().strftime("%d %B %Y")},
    {"id": "2", "name": "Smoothie Hijau", "description": "Smoothie dari sayuran hijau organik", "price": 25000, "created_at": datetime.now().strftime("%d %B %Y")},
]

class FoodList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(foods),
            "foods": foods
        }

    def post(self):
        data = request.get_json()
        new_food = {
            "id": str(len(foods) + 1),
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "created_at": datetime.now().strftime("%d %B %Y")
        }
        foods.append(new_food)
        return {
            "error": False,
            "message": "Food added successfully",
            "food": new_food
        }, 201

class FoodDetail(Resource):
    def get(self, food_id):
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            return {
                "error": False,
                "message": "success",
                "food": food
            }
        return {"error": True, "message": "Food not found"}, 404

    def put(self, food_id):
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            data = request.get_json()
            food["name"] = data.get("name", food["name"])
            food["description"] = data.get("description", food["description"])
            food["price"] = data.get("price", food["price"])
            return {
                "error": False,
                "message": "Food updated successfully",
                "food": food
            }
        return {"error": True, "message": "Food not found"}, 404

    def delete(self, food_id):
        global foods
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            foods = [f for f in foods if f["id"] != food_id]
            return {
                "error": False,
                "message": "Food deleted successfully"
            }
        return {"error": True, "message": "Food not found"}, 404

class FoodSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [f for f in foods if query in f['name'].lower() or query in f['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "foods": result
        }

# Menambahkan resource ke API
api.add_resource(FoodList, '/foods')
api.add_resource(FoodDetail, '/foods/<string:food_id>')
api.add_resource(FoodSearch, '/foods/search')

if __name__ == '__main__':
    app.run(debug=True)
