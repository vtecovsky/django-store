from django.contrib import admin
from products.models import ProductCategory, Product

"Регистрация моделей для добавления данных через админ панель сайта"
admin.site.register(Product)
admin.site.register(ProductCategory)
