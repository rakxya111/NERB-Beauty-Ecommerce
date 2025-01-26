from django.urls import path
from cart import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/',views.AddToCartView.as_view(),name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path("remove_cart/<int:product_id>/", views.RemoveFromCartView.as_view(), name="remove_cart"),
    path("remove_cart_all/<int:product_id>/", views.RemoveCartView.as_view(), name="remove_cart_all"),
    path("favourite_list/", views.FavouriteView.as_view(), name="favourite_list"),
    path("remove_favourite/<int:product_id>/", views.RemoveFromFavView.as_view(), name="remove_favourite"),
    path('add_favourites/<int:product_id>/',views.AddFavouriteView.as_view(), name='add_favourites'),
]