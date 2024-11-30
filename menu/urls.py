from . import views
from django.urls import path

urlpatterns = [
    path('', views.MenuList.as_view(), name="menu"),
    path('add/', views.MenuAdd.as_view(), name="menu-add"),
    path('<uuid:id>/', views.MenuItem.as_view(), name="menu-item"),
    path('<uuid:id>/update/', views.MenuUpdate.as_view(), name="menu-update"),
    path('<uuid:id>/delete/', views.MenuDelete.as_view(), name="menu-delete"),
    path('category/<uuid:category_id>/', views.MenuByCategory.as_view(), name='menu-by-category'),
    path('<uuid:item_id>/reviews/add', views.MenuReview.as_view(), name="menu-review"),
    path('<uuid:item_id>/reviews/<uuid:review_id>/update/', views.ReviewUpdate.as_view(), name="review-update"),
]
