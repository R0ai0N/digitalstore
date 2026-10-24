import shutil
import tempfile
from unittest import mock

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product, Favorite, ProductBasket, Order, Delivery

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ShopFlowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed', stdout=open(MEDIA_ROOT + '/seed.log', 'w'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def register(self):
        photo_path = 'shop/static/image/goods/user.jpg'
        with open(photo_path, 'rb') as f:
            photo = SimpleUploadedFile('user.jpg', f.read(), content_type='image/jpeg')
        return self.client.post(reverse('registration'), {
            'username': 'testuser',
            'first_name': 'Алексей',
            'last_name': 'Иванов',
            'email': 'test@example.com',
            'password1': 'StrongPass12345',
            'password2': 'StrongPass12345',
            'phone_number': '+998901234567',
            'photo': photo
        })

    def test_public_pages(self):
        product = Product.objects.get(slug='samsung-galaxy-a52-white')
        urls = [
            reverse('main'),
            reverse('category', kwargs={'slug': 'smartphones'}),
            reverse('category', kwargs={'slug': 'smartphones'}) + '?brand=samsung&model=galaxy-a52&price_from=1000000&price_to=5000000',
            reverse('category', kwargs={'slug': 'conditioners'}),
            product.get_absolute_url(),
            reverse('search') + '?q=Samsung',
            reverse('sale'),
            reverse('login'),
            reverse('registration'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Хиты продаж')
        self.assertContains(response, '/static/css/style.css')
        self.assertContains(response, 'Вход')
        self.assertContains(response, 'Смартфоны')
        self.assertContains(response, 'От 289 800 сум / 12 мес')

        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, 'Общие характеристики')
        self.assertContains(response, reverse('product', kwargs={'slug': 'samsung-galaxy-a52-black'}))

        response = self.client.get(reverse('search') + '?q=iPhone')
        self.assertContains(response, 'Apple iPhone 13 Pro Max')
        self.assertNotContains(response, 'Холодильник LG')

        response = self.client.get(reverse('category', kwargs={'slug': 'smartphones'}) + '?brand=xiaomi')
        self.assertContains(response, 'Redmi Note 11')
        self.assertNotContains(response, 'Apple iPhone 13 Pro Max</p>')

        self.assertEqual(self.client.get(reverse('category', kwargs={'slug': 'unknown'})).status_code, 404)

    def test_pagination(self):
        category = Category.objects.get(slug='smartphones')
        base = Product.objects.filter(category=category).first()
        for i in range(10):
            Product.objects.create(title=f'Тест {i}', slug=f'test-{i}', descr='test', category=category,
                                   brand=base.brand, model=base.model)

        url = reverse('category', kwargs={'slug': 'smartphones'})
        response = self.client.get(url + '?brand=samsung')
        self.assertContains(response, 'page-link-active')
        self.assertContains(response, '?brand=samsung&amp;page=2')
        self.assertEqual(self.client.get(url + '?brand=samsung&page=2').status_code, 200)

    def test_login_required_pages_redirect(self):
        for name in ['cart', 'checkout', 'profile', 'favorites']:
            response = self.client.get(reverse(name))
            self.assertRedirects(response, reverse('login') + '?next=' + reverse(name), fetch_redirect_response=False)

    @mock.patch('shop.views.stripe.checkout.Session.create')
    def test_full_flow(self, session_create):
        session_create.return_value = mock.Mock(url='https://checkout.stripe.test/session')

        response = self.register()
        self.assertRedirects(response, reverse('main'))
        user = User.objects.get(username='testuser')
        self.assertEqual(user.customer.phone, '+998901234567')
        self.assertTrue(user.customer.photo)
        self.assertTrue(user.customer.basket)

        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Профиль')
        self.assertContains(response, 'Выход')

        self.client.get(reverse('logout'))
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrong'}, follow=True)
        self.assertContains(response, 'id="message"')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'StrongPass12345'})
        self.assertRedirects(response, reverse('main'))

        product = Product.objects.get(slug='samsung-galaxy-a52-white')
        self.client.post(reverse('action_fav'), {'product_slug': product.slug})
        self.assertTrue(Favorite.objects.filter(user=user, product=product).exists())
        response = self.client.get(reverse('favorites'))
        self.assertContains(response, product.title)
        self.assertContains(response, 'fill="#0F2859"')
        self.client.post(reverse('action_fav'), {'product_slug': product.slug})
        self.assertFalse(Favorite.objects.filter(user=user, product=product).exists())
        self.client.post(reverse('action_fav'), {'product_slug': product.slug})

        cart_url = reverse('cart')
        self.client.post(reverse('action_basket'), {'product_slug': product.slug, 'action': 'add'}, HTTP_REFERER=cart_url)
        self.client.post(reverse('action_basket'), {'product_slug': product.slug, 'action': 'add'}, HTTP_REFERER=cart_url)
        self.client.post(reverse('action_basket'), {'product_slug': product.slug, 'action': 'delete'}, HTTP_REFERER=cart_url)
        item = ProductBasket.objects.get(basket=user.customer.basket, product=product)
        self.assertEqual(item.quantity, 1)

        product.quantity = 1
        product.save()
        response = self.client.post(reverse('action_basket'), {'product_slug': product.slug, 'action': 'add'},
                                    HTTP_REFERER=cart_url, follow=True)
        self.assertContains(response, 'Больше этого товара нет в наличии')
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

        other = Product.objects.get(slug='lg-gn-f372-sbcb')
        self.client.post(reverse('action_basket'), {'product_slug': other.slug, 'action': 'add'})
        response = self.client.get(cart_url)
        self.assertContains(response, product.title)
        self.assertContains(response, 'arrow-up.png')
        self.assertContains(response, reverse('clear_cart'))
        self.assertContains(response, reverse('checkout'))

        response = self.client.get(reverse('checkout'))
        self.assertContains(response, 'name="city"')
        self.assertContains(response, 'Сумма оплаты')

        response = self.client.post(reverse('payment'), {'first_name': 'Алексей'})
        self.assertRedirects(response, reverse('checkout'), fetch_redirect_response=False)
        session_create.assert_not_called()

        delivery = {
            'city': 'Ташкент', 'address': 'Шота Руставели 150', 'state': 'Ташкент', 'phone': '+998901234567',
            'comment': 'Позвонить заранее', 'first_name': 'Алексей', 'last_name': 'Иванов',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('payment'), delivery)
        self.assertRedirects(response, 'https://checkout.stripe.test/session', fetch_redirect_response=False)
        kwargs = session_create.call_args.kwargs
        self.assertEqual(kwargs['line_items'][0]['price_data']['currency'], 'uzs')
        self.assertEqual(kwargs['line_items'][0]['price_data']['unit_amount'],
                         (product.get_price() + other.get_price()) * 100)

        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(customer=user.customer)
        self.assertEqual(order.products.count(), 2)
        self.assertEqual(order.price, product.get_price() + other.get_price())
        self.assertEqual(Delivery.objects.get(order=order).city, 'Ташкент')
        self.assertFalse(user.customer.basket.products.exists())
        product.refresh_from_db()
        self.assertEqual(product.quantity, 0)

        self.assertRedirects(self.client.get(reverse('success')), reverse('main'))

        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Личный кабинет')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, product.title)
        self.assertContains(response, '/media/products/')

        self.client.post(reverse('action_basket'), {'product_slug': other.slug, 'action': 'add'})
        self.client.post(reverse('clear_cart'))
        self.assertFalse(user.customer.basket.products.exists())
        self.assertEqual(self.client.get(reverse('clear_cart')).status_code, 405)
        self.assertRedirects(self.client.get(reverse('checkout')), reverse('cart'))

    def test_superuser_without_customer(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass12345')
        self.client.login(username='admin', password='AdminPass12345')
        for name in ['cart', 'profile', 'favorites']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 200)
        self.assertEqual(self.client.get('/admin/shop/product/').status_code, 200)
        self.assertEqual(self.client.get('/admin/shop/category/1/change/').status_code, 200)
