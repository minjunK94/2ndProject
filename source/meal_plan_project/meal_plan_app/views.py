from django.shortcuts import render
import joblib
import pandas as pd

# 모델 불러오기
model = joblib.load("xgboost_meal_plan.pkl")

# 식품 데이터 불러오기 (CSV 파일 활용)
food_data = pd.read_csv("food_nutrition_data.csv")  # 식품별 영양 데이터
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def recommend_meal(request):
    if request.method == "POST":
        gender = request.POST.get("gender")
        body_type = request.POST.get("body_type")
        goal = request.POST.get("goal")

        # 임시로 출력 (여기에 식단 추천 로직 연결 가능)
        context = {
            "gender": gender,
            "body_type": body_type,
            "goal": goal,
            "recommended_calories": 2000,  # 여기에 XGBoost 모델 예측 값 넣기
            "recommended_carbs": 250,
            "recommended_protein": 100,
            "recommended_fat": 70,
            "breakfast": "귀리 + 바나나 + 우유",
            "lunch": "현미밥 + 닭가슴살 + 채소",
            "dinner": "고구마 + 삶은 계란 + 두부"
        }
        return render(request, "result.html", context)

    return render(request, "index.html")


def recommend(request):
    if request.method == "POST":
        # 사용자 입력값 받기
        gender = request.POST.get("gender")
        body_type = request.POST.get("body_type")
        goal = request.POST.get("goal")

        # 입력값을 모델의 형식에 맞게 변환
        input_data = pd.DataFrame([[gender, body_type, goal]], columns=["성별", "체형", "목표"])

        # 칼로리 및 탄단지 예측
        y_pred = model.predict(input_data)
        total_calories, carbs, protein, fat = y_pred[0]

        # 식단 구성 모델 (탄단지 비율을 기반으로 아침, 점심, 저녁 식단 추천)
        meal_plan = generate_meal_plan(total_calories, carbs, protein, fat)

        return render(request, "result.html", {
            "total_calories": round(total_calories, 2),
            "carbs": round(carbs, 2),
            "protein": round(protein, 2),
            "fat": round(fat, 2),
            "meal_plan": meal_plan  # 추천된 아침, 점심, 저녁 식단
        })
    return render(request, "index.html")


def generate_meal_plan(total_calories, carbs, protein, fat):
    """ 탄단지 비율을 기반으로 아침, 점심, 저녁 식단 구성 """
    # 아침(균형식), 점심(고단백), 저녁(저탄수) 기준으로 분배
    breakfast = food_data[food_data["category"] == "breakfast"].sample(3).to_dict(orient="records")
    lunch = food_data[food_data["category"] == "lunch"].sample(3).to_dict(orient="records")
    dinner = food_data[food_data["category"] == "dinner"].sample(3).to_dict(orient="records")

    return {"breakfast": breakfast, "lunch": lunch, "dinner": dinner}
