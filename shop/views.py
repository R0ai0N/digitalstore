# делала по видосам из класса, но чисто я просто брала и изменяла код из loft и нашего
# gameproject
# для импорта в некоторых местах нажимала на alt + enter
# походу писания кода использовала 2 метода как было на уроках, и классы и функции :)
# в некоторых местах подумала что генераторы могут сократить количество кода и сделать более читабельнее

import os

import stripe
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from dotenv import load_dotenv

from .config import filter_products
from .forms import LoginForm, RegisterUserForm, DeliveryForm
from .models import Category, Brand, ModelProduct, Product, Banner, Promo, Customer, Basket, Favorite
from .utils import BasketAuthCustomer


def main_page_view(request):
    context = {
        'title': 'Интернет магазин цифровой и бытовой техники',
        'banners': Banner.objects.all(),
        'hits': Product.objects.filter(is_hit=True).order_by('-created_at')[:8],
        'new_products': Product.objects.all().order_by('-created_at')[:8],
        'promos': Promo.objects.all()
    }

    return render(request, 'shop/index.html', context)


class ProductByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'
    # пагинация по 8 товаров на страницу, кажеться тогда по 2 получаеться
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        # если что то идёт не так выдаёт - ошибка 404
        products = Product.objects.filter(category=self.category)
        products = filter_products(self.request, products)
        return products.order_by('-created_at')
    # created at - сначала новые по убыванию

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(category=self.category)
        brand = self.request.GET.get('brand')
        if brand:
            products = products.filter(brand__slug=brand)

        context['title'] = self.category.title
        context['category'] = self.category
        context['brands'] = Brand.objects.filter(products__category=self.category).distinct()
        # distinct - убирает дубли
        context['models'] = ModelProduct.objects.filter(products__in=products).distinct()
        context['current_brand'] = Brand.objects.filter(slug=brand).first()
        context['current_model'] = ModelProduct.objects.filter(slug=self.request.GET.get('model')).first()
        context['prices'] = [i for i in range(1000000, 31000000, 1000000)]
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context.get('product')
        context['title'] = product.title
        context['product_colors'] = Product.objects.filter(model=product.model, category=product.category)
        same_products = Product.objects.filter(category=product.category).exclude(model=product.model)
        context['same_products'] = same_products.order_by('-created_at')[:4]
        return context


def search_products_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(title__icontains=query).order_by('-created_at') if query else []
    # __icontains - SQL, без учёта регистра, если запрос пустой, возвращается пустой список
    context = {
        'title': f'Результаты поиска: {query}',
        'products': products
    }
    return render(request, 'shop/products.html', context)


def login_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main')

        messages.error(request, 'Неверное имя пользователя или пароль')
        return redirect('login')

    context = {
        'title': 'Авторизация',
        'form': LoginForm()
    }
    return render(request, 'shop/login.html', context)


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            customer = Customer.objects.create(user=user, phone=form.cleaned_data['phone_number'],
                                               photo=form.cleaned_data.get('photo'))
            Basket.objects.create(customer=customer)
            login(request, user)
            return redirect('main')

        for key in form.errors:
            messages.error(request, form.errors[key].as_text())
        return redirect('registration')

    context = {
        'title': 'Регистрация',
        'form': RegisterUserForm()
    }
    return render(request, 'shop/registration.html', context)


def logout_user_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main')


# дальше с деокараторами, и для авторизированных юзеров
@login_required(login_url='login')
@require_POST
def action_favorite(request):
    product = get_object_or_404(Product, slug=request.POST.get('product_slug'))
    favorite, created = Favorite.objects.get_or_create(product=product, user=request.user)
    if not created:
        favorite.delete()

    next_page = request.META.get('HTTP_REFERER', 'main')
    return redirect(next_page)


@login_required(login_url='login')
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'title': 'Избранное',
        'products': [i.product for i in favorites]
    }
    return render(request, 'shop/products.html', context)


def sale_products_view(request):
    products = Product.objects.filter(discount__gt=0).order_by('-created_at')
    context = {
        'title': 'Товары со скидкой',
        'products': products
    }
    return render(request, 'shop/products.html', context)


@login_required(login_url='login')
@require_POST
def action_basket_customer(request):
    slug = request.POST.get('product_slug')
    action = request.POST.get('action')
    get_object_or_404(Product, slug=slug)
    basket = BasketAuthCustomer(request, slug, action)
    if basket.error:
        messages.error(request, basket.error)

    next_page = request.META.get('HTTP_REFERER', 'main')
    return redirect(next_page)


@login_required(login_url='login')
@require_POST
def clear_basket_view(request):
    basket = BasketAuthCustomer(request)
    basket.clear_basket()
    return redirect('cart')


@login_required(login_url='login')
def customer_basket_view(request):
    basket = BasketAuthCustomer(request)
    context = basket.customer_basket()
    context['title'] = 'Моя корзина'
    return render(request, 'shop/card_goods.html', context)


@login_required(login_url='login')
def checkout_view(request):
    basket = BasketAuthCustomer(request)
    context = basket.customer_basket()
    if not context['products']:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart')

    user = request.user
    context['form'] = DeliveryForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': context['customer'].phone
    })
    context['title'] = 'Оформление заказа'
    return render(request, 'shop/make_order.html', context)


@login_required(login_url='login')
@require_POST
def create_checkout_session(request):
    # нужна для загрузки из env, что то секретное
    load_dotenv()
    basket = BasketAuthCustomer(request)
    info = basket.customer_basket()
    if not info['products']:
        return redirect('main')

    form = DeliveryForm(data=request.POST)
    if not form.is_valid():
        for key in form.errors:
            messages.error(request, form.errors[key].as_text())
        return redirect('checkout')

    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'uzs',
                'product_data': {'name': ', '.join(i.product.title for i in info['products'])},
                'unit_amount': int(info['basket_price']) * 100
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('checkout'))
    )
    request.session[f'delivery_{request.user.pk}'] = form.cleaned_data
    return redirect(session.url)


@login_required(login_url='login')
def success_payment_view(request):
    basket = BasketAuthCustomer(request)
    data = basket.customer_basket()
    form_data = request.session.pop(f'delivery_{request.user.pk}', None)

    if not data['products'] or not form_data:
        return redirect('main')

    form = DeliveryForm(data=form_data)
    if not form.is_valid():
        return redirect('checkout')

    delivery = form.save(commit=False)
    delivery.customer = data['customer']
    delivery.save()
    basket.save_order_customer(delivery)

    context = {'title': 'Успешная оплата'}
    return render(request, 'shop/success.html', context)


@login_required(login_url='login')
def profile_customer(request):
    customer = BasketAuthCustomer(request).customer_basket()['customer']
    context = {
        'title': 'Личный кабинет',
        'customer': customer,
        'orders': customer.orders.all().order_by('-created_at')
    }
    return render(request, 'shop/profile.html', context)


