from django.urls import path
from mainshop import views


urlpatterns = [
    
    path("",views.HomeView.as_view(),name="home"),
    path('featured-products/', views.FeaturedProductsView.as_view(), name='featured-products'), 
    path('featured-products/<slug:category_slug>/', views.FeaturedProductsView.as_view(),name='featured-products-by-category'),  
    path('ajax/featured-products/<slug:category_slug>/', views.ajax_featured_products, name='ajax-featured-products'),
    path("product-list/",views.ProductListView.as_view(),name="product-list"),
    path("product-by-category/<int:category_id>/",views.PostByCategoryView.as_view(),name="product-by-category"),
    path("product-by-brand/<int:brand_id>/",views.PostByBrandView.as_view(),name="product-by-brand"),
    path("product-detail/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("product-search/",views.ProductSearchView.as_view(),name="product-search"),
   

]