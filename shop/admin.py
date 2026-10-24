from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm

admin.site.register(Customer)
admin.site.register(Favorite)
admin.site.register(Basket)
admin.site.register(ProductBasket)
admin.site.register(Delivery)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm
    list_display = ('pk', 'title', 'get_icon')
    list_display_links = ('pk', 'title')

    def get_icon(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" width="30">')
        else:
            return 'No icon'

    get_icon.short_description = 'Иконка'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title')


@admin.register(ModelProduct)
class ModelProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title')


class ImagesInline(admin.TabularInline):
    model = ImagesProduct
    fk_name = 'product'
    extra = 1


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    fk_name = 'product'
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'discount', 'is_hit', 'color_name', 'category', 'get_photo')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImagesInline, CharacteristicInline]
    list_editable = ('price', 'quantity', 'discount', 'is_hit')
    list_filter = ('category', 'brand', 'is_hit')
    search_fields = ('title',)

    def get_photo(self, obj):
        if obj.first_photo():
            return mark_safe(f'<img src="{obj.first_photo()}" width="60">')
        else:
            return 'No photo'

    get_photo.short_description = 'Фото'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'descr')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    fk_name = 'order'
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'price', 'status', 'created_at')
    list_editable = ('status',)
    inlines = [ProductOrderInline]
