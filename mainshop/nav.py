from mainshop.models import Category,Brand,Product
from cart.models import Cart, CartItem

def navigation(request):
    categories = Category.objects.all()[:15]
    featured_categories = Category.objects.all()[:5]
    brands = Brand.objects.all()
    latest_products_list = Product.objects.all().order_by('-created_date')[:9] 
    sale_product_list = Product.objects.filter(is_available=True,is_sale=True).order_by('-created_date')[:9]
    latest_products = [latest_products_list[i:i+3] for i in range(0, len(latest_products_list), 3)] 
    sale_products = [sale_product_list[i:i+3] for i in range(0,len(sale_product_list), 3)]



   
    return{
        
        "categories" : categories,
        "brands" : brands,
        "featured_categories" : featured_categories,
        "latest_products" : latest_products,
        "sale_products" : sale_products,
        

    }

