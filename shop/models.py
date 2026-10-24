# models kak struktura bazi dannih, po nim vedyotsya migratsiya, kak klass tablitsa, a pole kolonka
# я не стала сильно менять models всё по принципу наших классных rabot
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, verbose_name='Иконка')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # показывает какой url ведёт на страницу определённую
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        # Meta - доп настройка самой модели, остальное не помню :(
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название бренда')
    slug = models.SlugField(unique=True, verbose_name='Слаг бренда')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class ModelProduct(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название модели')
    slug = models.SlugField(unique=True, verbose_name='Слаг модели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели товаров'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара')
    descr = models.CharField(max_length=400, verbose_name='Описание')
    price = models.IntegerField(default=1000000, verbose_name='Стоимость товара')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
    quantity = models.IntegerField(default=15, verbose_name='Количество товара')
    color_name = models.CharField(max_length=50, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=20, default='#ffffff', verbose_name='Код цвета')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория товара', related_name='products')
    # foreignkey - for connecting 1 table with other
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='products')
    model = models.ForeignKey(ModelProduct, on_delete=models.CASCADE, verbose_name='Модель товара',
                              related_name='products')
    guarantee = models.CharField(max_length=50, default='1 год', verbose_name='Гарантия')
    is_hit = models.BooleanField(default=False, verbose_name='Хит продаж')
    # bool - true or false, no other type
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    def first_photo(self):
        image = self.images.first()
        if image:
            return image.photo.url
        else:
            return ''

    def get_price(self):
        if self.discount:
            p = self.price - (self.price * self.discount / 100)
        else:
            p = self.price

        return int(p)

    def get_month_price(self):
        return self.get_price() // 12

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ImagesProduct(models.Model):
    photo = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')

    def __str__(self):
        return f'Фото товара {self.product.title}'

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар',
                                related_name='characteristics')
    name = models.CharField(max_length=150, verbose_name='Название')
    value = models.CharField(max_length=300, verbose_name='Значение')

    def __str__(self):
        return f'{self.name}: {self.value}'

    class Meta:
        verbose_name = 'Характеристику'
        verbose_name_plural = 'Характеристики'


class Banner(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    descr = models.CharField(max_length=300, verbose_name='Текст')
    image = models.ImageField(upload_to='banners/', verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class Promo(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название акции')
    image = models.ImageField(upload_to='promos/', verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акцию'
        verbose_name_plural = 'Акции'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=40, blank=True, verbose_name='Номер телефона')
    photo = models.ImageField(upload_to='customers/', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return f'Покупатель {self.user.last_name} {self.user.first_name}'

    class Meta:
        verbose_name = 'Покупателя'
        verbose_name_plural = 'Покупатели'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'Товар {self.product.title} пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Basket(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Корзина №: {self.pk} покупателя {self.customer.user.username}'

    @property
    def basket_price(self):
        product_basket = self.products.all()
        price = sum([i.get_total_price for i in product_basket])
        return price

    @property
    def quantity_products(self):
        product_basket = self.products.all()
        quantity = sum([i.quantity for i in product_basket])
        return quantity

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины покупателей'


class ProductBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='Корзина', related_name='products')
    quantity = models.IntegerField(default=0, verbose_name='Кол-во')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Товар {self.product.title} в кол-ве {self.quantity}'

    @property
    def get_total_price(self):
        return int(self.quantity * self.product.get_price())

    class Meta:
        verbose_name = 'Товар Корзины'
        verbose_name_plural = 'Товары Корзин'


class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    first_name = models.CharField(max_length=255, verbose_name='Имя получателя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия получателя')
    email = models.EmailField(blank=True, verbose_name='Почта')
    phone = models.CharField(max_length=255, blank=True, verbose_name='Номер получателя')
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    state = models.CharField(max_length=255, verbose_name='Регион')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Доставка №: {self.pk} для {self.customer}'

    class Meta:
        verbose_name = 'Доставку'
        verbose_name_plural = 'Доставки'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='orders')
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, verbose_name='Доставка')
    price = models.IntegerField(default=0, verbose_name='Стоимость заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.BooleanField(default=False, verbose_name='Статус заказа')

    def __str__(self):
        return f'Заказ №: {self.pk} {self.customer} на сумму: {self.price}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы покупателей'


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='products')
    title = models.CharField(max_length=300, verbose_name='Название товара')
    slug = models.CharField(max_length=300, verbose_name='Слаг товара')
    price = models.IntegerField(default=0, verbose_name='Цена товара')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    total_price = models.IntegerField(default=0, verbose_name='На сумму')
    photo = models.ImageField(upload_to='orders/', blank=True, verbose_name='Фото товара')

    def __str__(self):
        return f'Товар {self.title} заказа №: {self.order.pk}'

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'
