from django.shortcuts import render
from django.urls import reverse
from mainshop.models import Product , Category , Brand,Newsletter,Contact
from django.views.generic import ListView,TemplateView,DetailView,View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from mainshop.forms import Newsletterform,ContactForm

class HomeView(ListView):
    model = Product
    template_name = "mainshop/home.html"
    context_object_name = "products"
    queryset = Product.objects.filter(
        is_available=True
    ).order_by("-created_date")[:8]

class FeaturedProductsView(ListView):
    model = Product
    template_name = 'mainshop/base.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug", None)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Product.objects.filter(is_available=True, category=category).order_by("-created_date")
        return Product.objects.filter(is_available=True).order_by("-created_date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.all()
        context['selected_category'] = self.kwargs.get("category_slug", 'all')
        return context

def ajax_featured_products(request, category_slug):
    if category_slug == 'all':
        products = Product.objects.filter(is_available=True).order_by("-created_date")[:8]
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category).order_by("-created_date")[:8]
    
    products_data = [
        {
            'product_name': product.product_name,
            'price': product.price,
            'discount' : product.discount,
            'price': float(product.price) if product.price else 0.0,
            'sale_price': float(product.sale_price()) if product.is_sale else 0.0,  # Call the method
            'discount': float(product.discount) if product.discount else 0.0,
            'is_sale': product.is_sale,
            'image_url': product.images.first().image.url if product.images.exists() else '',
            'category_slug': product.category.slug,
            'pk': product.pk,  
        }
        for product in products
    ]
    return JsonResponse({'products': products_data})



class ProductListView(ListView):
    model = Product
    template_name = "mainshop/store/store.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        sort = self.request.GET.get("sort")

        if sort == "price_asc":
            queryset = queryset.order_by("price")  # Low to high
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")  # High to low
        elif sort == "sale_product":
            queryset = Product.objects.filter(is_available=True,is_sale=True).order_by("-created_date")


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_count"] = self.get_queryset().count()
        context["request"] = self.request  # Pass request to template
        return context

class PostByCategoryView(ListView):
    model = Product
    template_name = "mainshop/store/store.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        if category_id:
            queryset = queryset.filter(
                is_available=True,
                category__id=category_id
            ).order_by("-created_date")
        
        sort_option = self.request.GET.get('sort')
        if sort_option == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-price')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.kwargs.get("category_id", 'all')
        context['product_count'] = self.get_queryset().count()
        return context



class PostByBrandView(ListView):
    model = Product
    template_name = "mainshop/store/store.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.kwargs.get("brand_id")
        if brand_id:
            queryset = queryset.filter(
                is_available=True,
                brand__id=brand_id
            ).order_by("-created_date")
        
        sort_option = self.request.GET.get('sort')
        if sort_option == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-price')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['selected_brand'] = self.kwargs.get("brand_id", 'all')
        context['product_count'] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "mainshop/product_detail/main_productDetail.html"
    context_object_name = "product"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_available=True)
        return query
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        context['related_products'] = related_products
        return context

class ProductSearchView(View):
    template_name = "mainshop/store/store.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")  # Use .get() to avoid KeyError
        product_list = Product.objects.filter(
            (Q(product_name__icontains=query) |
             Q(description__icontains=query)) &
            Q(is_available=True)
        ).order_by("-created_date")
        
        # Pagination start
        page = request.GET.get("page", 1)  # Default page is 1
        paginate_by = 10
        paginator = Paginator(product_list, paginate_by)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        # Pagination end

        return render(
            request,
            self.template_name,
            {"page_obj": products, "query": query},
        )
     
class NewsletterView(View):
    def post(self, request):
        is_ajax = request.headers.get("X-Requested-With")
        if is_ajax == "XMLHttpRequest":
            form = Newsletterform(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                
                # Check for duplicate email
                if Newsletter.objects.filter(email=email).exists():
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "This email is already subscribed to the newsletter.",
                        },
                        status=400,
                    )
                
                # Save the form if no duplicates
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully Subscribed to Newsletter",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot Subscribe to the Newsletter. Please check your input.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process, must be an AJAX XMLHttpRequest.",
                },
                status=400,
            )

