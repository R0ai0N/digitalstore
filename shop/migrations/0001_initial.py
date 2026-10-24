
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('descr', models.CharField(max_length=300, verbose_name='Текст')),
                ('image', models.ImageField(upload_to='banners/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название бренда')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг бренда')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг категории')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='icons/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ModelProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название модели')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг модели')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели товаров',
            },
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название акции')),
                ('image', models.ImageField(upload_to='promos/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Акцию',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Номер телефона')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='customers/', verbose_name='Фото')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупателя',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Корзину',
                'verbose_name_plural': 'Корзины покупателей',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя получателя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия получателя')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='Номер получателя')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('state', models.CharField(max_length=255, verbose_name='Регион')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Доставку',
                'verbose_name_plural': 'Доставки',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='Стоимость заказа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('status', models.BooleanField(default=False, verbose_name='Статус заказа')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shop.customer', verbose_name='Покупатель')),
                ('delivery', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.delivery', verbose_name='Доставка')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы покупателей',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название товара')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг товара')),
                ('descr', models.CharField(max_length=400, verbose_name='Описание')),
                ('price', models.IntegerField(default=1000000, verbose_name='Стоимость товара')),
                ('discount', models.IntegerField(default=0, verbose_name='Скидка')),
                ('quantity', models.IntegerField(default=15, verbose_name='Количество товара')),
                ('color_name', models.CharField(default='Белый', max_length=50, verbose_name='Название цвета')),
                ('color_code', models.CharField(default='#ffffff', max_length=20, verbose_name='Код цвета')),
                ('guarantee', models.CharField(default='1 год', max_length=50, verbose_name='Гарантия')),
                ('is_hit', models.BooleanField(default=False, verbose_name='Хит продаж')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Категория товара')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.modelproduct', verbose_name='Модель товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ImagesProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='products/', verbose_name='Фото товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фото товара',
                'verbose_name_plural': 'Фото товаров',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('value', models.CharField(max_length=300, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Характеристику',
                'verbose_name_plural': 'Характеристики',
            },
        ),
        migrations.CreateModel(
            name='ProductBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Кол-во')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.basket', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар Корзины',
                'verbose_name_plural': 'Товары Корзин',
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название товара')),
                ('slug', models.CharField(max_length=300, verbose_name='Слаг товара')),
                ('price', models.IntegerField(default=0, verbose_name='Цена товара')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('total_price', models.IntegerField(default=0, verbose_name='На сумму')),
                ('photo', models.ImageField(blank=True, upload_to='orders/', verbose_name='Фото товара')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Товар заказа',
                'verbose_name_plural': 'Товары заказов',
            },
        ),
    ]
