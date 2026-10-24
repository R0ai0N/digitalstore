from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from shop.models import Category, Brand, ModelProduct, Product, ImagesProduct, Characteristic, Banner, Promo

IMAGES = settings.BASE_DIR / 'shop' / 'static' / 'image'

CATEGORIES = [
    ('Смартфоны', 'smartphones', 'phone.svg'),
    ('Ноутбуки', 'laptops', 'book.svg'),
    ('Телевизоры', 'tv', 'tv.svg'),
    ('Кондиционеры', 'conditioners', 'condition.svg'),
    ('Холодильники', 'refrigerators', 'refrigerator.svg'),
]

BRANDS = [
    ('Samsung', 'samsung'),
    ('Apple', 'apple'),
    ('Xiaomi', 'xiaomi'),
    ('ASUS', 'asus'),
    ('LG', 'lg'),
]

PRODUCTS = [
    {
        'title': 'Смартфон Samsung Galaxy A52 White 128Gb', 'slug': 'samsung-galaxy-a52-white',
        'category': 'smartphones', 'brand': 'samsung', 'model': ('Galaxy A52', 'galaxy-a52'),
        'price': 3864000, 'discount': 10, 'color_name': 'Белый', 'color_code': '#ffffff',
        'is_hit': True, 'guarantee': '1 год', 'photo': 'Rectangle 356 (2).png',
        'characteristics': [('Марка и модель', 'Samsung Galaxy A52'), ('Размер (Диагональ)', '6.5" (дюйма)'),
                            ('Аккумулятор', '4500 мАч, Li-Po'), ('Операционная система(OS)', 'Android 11, One UI 3.1')],
    },
    {
        'title': 'Смартфон Samsung Galaxy A52 Black 128Gb', 'slug': 'samsung-galaxy-a52-black',
        'category': 'smartphones', 'brand': 'samsung', 'model': ('Galaxy A52', 'galaxy-a52'),
        'price': 3864000, 'discount': 0, 'color_name': 'Чёрный', 'color_code': '#323232',
        'is_hit': False, 'guarantee': '1 год', 'photo': 'Rectangle 356 (2).png',
        'characteristics': [('Марка и модель', 'Samsung Galaxy A52'), ('Размер (Диагональ)', '6.5" (дюйма)'),
                            ('Аккумулятор', '4500 мАч, Li-Po'), ('Операционная система(OS)', 'Android 11, One UI 3.1')],
    },
    {
        'title': 'Смартфон Samsung Galaxy S22 Ultra 12/256GB', 'slug': 'samsung-galaxy-s22-ultra',
        'category': 'smartphones', 'brand': 'samsung', 'model': ('Galaxy S22 Ultra', 'galaxy-s22-ultra'),
        'price': 14990000, 'discount': 0, 'color_name': 'Чёрный', 'color_code': '#323232',
        'is_hit': True, 'guarantee': '1 год', 'photo': 'Rectangle 356 (6).png',
        'characteristics': [('Марка и модель', 'Samsung Galaxy S22 Ultra'), ('Размер (Диагональ)', '6.8" (дюйма)'),
                            ('Аккумулятор', '5000 мАч, Li-Ion')],
    },
    {
        'title': 'Apple iPhone 13 Pro Max RM/A 6/128GB', 'slug': 'apple-iphone-13-pro-max',
        'category': 'smartphones', 'brand': 'apple', 'model': ('iPhone 13 Pro Max', 'iphone-13-pro-max'),
        'price': 16729000, 'discount': 0, 'color_name': 'Голубой', 'color_code': '#4769b8',
        'is_hit': True, 'guarantee': '1 год', 'photo': 'Rectangle 356 (1).png',
        'characteristics': [('Марка и модель', 'Apple iPhone 13 Pro Max'), ('Размер (Диагональ)', '6.7" (дюйма)'),
                            ('Операционная система(OS)', 'iOS 15')],
    },
    {
        'title': 'Смартфон Xiaomi Redmi Note 11 4/128GB', 'slug': 'xiaomi-redmi-note-11',
        'category': 'smartphones', 'brand': 'xiaomi', 'model': ('Redmi Note 11', 'redmi-note-11'),
        'price': 2590000, 'discount': 15, 'color_name': 'Серый', 'color_code': '#7787a6',
        'is_hit': True, 'guarantee': '1 год', 'photo': 'Redmi.png',
        'characteristics': [('Марка и модель', 'Xiaomi Redmi Note 11'), ('Аккумулятор', '5000 мАч, Li-Po')],
    },
    {
        'title': 'Смартфон Xiaomi 11 Lite 5G NE 8/128GB', 'slug': 'xiaomi-11-lite-5g-ne',
        'category': 'smartphones', 'brand': 'xiaomi', 'model': ('11 Lite 5G NE', '11-lite-5g-ne'),
        'price': 4390000, 'discount': 0, 'color_name': 'Голубой', 'color_code': '#b3c7f0',
        'is_hit': False, 'guarantee': '1 год', 'photo': 'Xiaomi.png',
        'characteristics': [('Марка и модель', 'Xiaomi 11 Lite 5G NE'), ('Размер (Диагональ)', '6.55" (дюйма)')],
    },
    {
        'title': 'Ноутбук ASUS E410MA-202 Blue, 14" HD LED, Celeron N4020', 'slug': 'asus-e410ma-202-blue',
        'category': 'laptops', 'brand': 'asus', 'model': ('E410MA', 'e410ma'),
        'price': 3619000, 'discount': 0, 'color_name': 'Синий', 'color_code': '#4769b8',
        'is_hit': False, 'guarantee': '1 год', 'photo': 'Nout.png',
        'characteristics': [('Процессор', 'Intel Celeron N4020'), ('Экран', '14" HD LED'), ('Память', '4 ГБ / 128 ГБ')],
    },
    {
        'title': 'Телевизор Samsung 65AU8000 4K UHD Smart TV', 'slug': 'samsung-65au8000',
        'category': 'tv', 'brand': 'samsung', 'model': ('65AU8000', '65au8000'),
        'price': 16729000, 'discount': 5, 'color_name': 'Чёрный', 'color_code': '#323232',
        'is_hit': False, 'guarantee': '3 года', 'photo': 'Tv.png',
        'characteristics': [('Диагональ', '65"'), ('Разрешение', '4K UHD'), ('Smart TV', 'Tizen')],
    },
    {
        'title': 'Холодильник LG GN-F372 SBCB', 'slug': 'lg-gn-f372-sbcb',
        'category': 'refrigerators', 'brand': 'lg', 'model': ('GN-F372', 'gn-f372'),
        'price': 3864000, 'discount': 0, 'color_name': 'Чёрный', 'color_code': '#323232',
        'is_hit': False, 'guarantee': '2 года', 'photo': 'Refrigerator.png',
        'characteristics': [('Объём', '312 л'), ('Система No Frost', 'Да')],
    },
]

BANNERS = [
    ('Samsung Galaxy A72', 'Все, что вы любите – неповторимо'),
    ('Samsung Galaxy A52', 'Все, что вы любите – неповторимо'),
]

PROMOS = [
    ('Скидки на смартфоны', 'Rectangle 357.png'),
    ('Техника для дома', 'Rectangle 358.png'),
]


def image_file(folder, name):
    return File(open(IMAGES / folder / name, 'rb'), name=name)


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):
        for title, slug, icon in CATEGORIES:
            category, created = Category.objects.get_or_create(slug=slug, defaults={'title': title})
            if not category.icon:
                category.icon = image_file('icons', icon)
                category.save()

        for title, slug in BRANDS:
            Brand.objects.get_or_create(slug=slug, defaults={'title': title})

        for item in PRODUCTS:
            model_title, model_slug = item['model']
            model, created = ModelProduct.objects.get_or_create(slug=model_slug, defaults={'title': model_title})
            product, created = Product.objects.get_or_create(slug=item['slug'], defaults={
                'title': item['title'],
                'descr': item['title'],
                'price': item['price'],
                'discount': item['discount'],
                'color_name': item['color_name'],
                'color_code': item['color_code'],
                'is_hit': item['is_hit'],
                'guarantee': item['guarantee'],
                'category': Category.objects.get(slug=item['category']),
                'brand': Brand.objects.get(slug=item['brand']),
                'model': model,
            })
            if created:
                ImagesProduct.objects.create(product=product, photo=image_file('goods', item['photo']))
                for name, value in item['characteristics']:
                    Characteristic.objects.create(product=product, name=name, value=value)

        if not Banner.objects.exists():
            for title, descr in BANNERS:
                Banner.objects.create(title=title, descr=descr, image=image_file('advertising', 'Group 539.png'))

        if not Promo.objects.exists():
            for title, photo in PROMOS:
                Promo.objects.create(title=title, image=image_file('advertising', photo))

        self.stdout.write(self.style.SUCCESS('Тестовые данные добавлены'))
