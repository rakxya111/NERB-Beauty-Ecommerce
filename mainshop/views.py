from django.shortcuts import render
from django.urls import reverse
from mainshop.models import Product , Category , Brand
from django.views.generic import ListView,TemplateView,DetailView,View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

class HomeView(ListView):
    model = Product
    template_name = "mainshop/home.html"
    context_object_name = "products"
    queryset = Product.objects.filter(
        is_available=True
    )[:8]

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
        products = Product.objects.filter(is_available=True, category=category).order_by("-created_date")
    
    products_data = [
        {
            'product_name': product.product_name,
            'price': product.price,
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
     
