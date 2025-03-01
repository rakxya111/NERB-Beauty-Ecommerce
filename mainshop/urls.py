from django.urls import path
from mainshop import views


urlpatterns = [
    
    path("",views.HomeView.as_view(),name="home"),
    path('featured-products/', views.FeaturedProductsView.as_view(), name='featured-products'), 
    path('featured-products/<slug:category_slug>/', views.FeaturedProductsView.as_view(),name='featured-products-by-category'),  
    path('ajax-featured-products/<slug:category_slug>/', views.ajax_featured_products, name='ajax-featured-products'),
    path("product-list/",views.ProductListView.as_view(),name="product-list"),
    path("product-by-category/<int:category_id>/",views.PostByCategoryView.as_view(),name="product-by-category"),
    path("product-by-brand/<int:brand_id>/",views.PostByBrandView.as_view(),name="product-by-brand"),
    path("product-detail/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("product-search/",views.ProductSearchView.as_view(),name="product-search"),
    path("newsletter/",views.NewsletterView.as_view(),name="newsletter"),
    path("contact/",views.ContactView.as_view(),name="contact"),
    path("flash-sale/",views.FlashSaleView.as_view(),name="flash-sale"),
    path("about/",views.AboutView.as_view(),name="about"),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),
   

]