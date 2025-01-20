# from django_summernote.widgets import SummernoteWidget
# from django import forms
# from mainshop.models import Product

# class PostForm(forms.ModelForm):

#     class Meta:
#         model = Product
#         exclude = ("published_date")
#         widgets = {
#             "title" : forms.TextInput(
#                 attrs={
#                     "class":"form-control",
#                     "placeholder":"Enter the title of the post",
#                 }
#             ),
#             "content" : SummernoteWidget(
#                 attrs={
#                     "summernote":{
#                         "width" : "100%",
#                         "height" : "400px",
#                     },
#                 }
#             ),
#             "brand" : forms.Select(attrs={"class":"form-control"}),
#             "category" : forms.Select(attrs={"class":"form-control"}),
            
#         }