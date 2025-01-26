from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampModel):
    cat_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to="post_images/%Y/%m/%d",blank=True)

    def __str__(self):
        return self.cat_name

class Brand(TimeStampModel):
    brand_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    brand_image = models.ImageField(upload_to="brand_images/%Y/%m/%d",blank=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_sale = models.BooleanField(default=False) 
    discount = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    

    def sale_price(self):
        discount_amount = (self.price * self.discount) / 100
        saleprice = self.price - discount_amount
        return saleprice


    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', blank=False)

    def __str__(self):
        return f"Image for {self.product.product_name}"

class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class Newsletter(TimeStampModel):
    email = models.EmailField()

    def __str__(self):
        return self.email

