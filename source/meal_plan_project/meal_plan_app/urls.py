from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 홈 화면
    path('recommend/', views.recommend_meal, name='recommend_meal'),  # 식단 추천 결과
]
