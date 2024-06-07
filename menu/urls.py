from . import views
from django.urls import path

urlpatterns = [
    path('', views.menu, name="menu"),
    path('add/', views.add, name="menu_add"),
    path('<uuid:id>/update/', views.update, name="menu_update"),
    path('<uuid:id>/delete/', views.delete, name="menu_delete"),
    path('category/<uuid:category_id>/', views.menu_by_category, name='menu_by_category'),
    path('<uuid:id>/', views.menu_item, name="menu_item"),
    path('<uuid:item_id>/review/', views.review, name="menu_review"),
    path('reviews/<uuid:review_id>/update/', views.review_update, name="review_update"),
]
