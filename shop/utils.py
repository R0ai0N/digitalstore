from .models import Customer, Basket, ProductBasket, Product, Order, ProductOrder


# просто открывает корзину и меняет её
class BasketAuthCustomer:
    def __init__(self, request, slug=None, action=None):
        self.user = request.user
        self.error = None

        if slug and action:
            self.add_or_delete(slug, action)

    def customer_basket(self):
        customer, created = Customer.objects.get_or_create(user=self.user)
        # get or create - получи или создай, если есть то получит, если нет то создаст после проверки
        basket, created = Basket.objects.get_or_create(customer=customer)
        products = basket.products.all().order_by('added_at')

        basket_price = basket.basket_price
        basket_quantity = basket.quantity_products

        return {
            'basket': basket,
            'products': products,
            'customer': customer,
            'basket_price': basket_price,
            'basket_quantity': basket_quantity
        }

    def add_or_delete(self, slug, action):
        basket = self.customer_basket()['basket']
        product = Product.objects.get(slug=slug)
        product_basket, created = ProductBasket.objects.get_or_create(basket=basket, product=product)

        if action == 'add':
            if product.quantity > product_basket.quantity:
                product_basket.quantity += 1
            else:
                self.error = 'Больше этого товара нет в наличии'
        elif action == 'delete':
            product_basket.quantity -= 1

        product_basket.save()

        if product_basket.quantity <= 0:
            product_basket.delete()

    def save_order_customer(self, delivery):
        data = self.customer_basket()
        order = Order.objects.create(customer=data['customer'], price=data['basket_price'], delivery=delivery)
        for item in data['products']:
            image = item.product.images.first()
            ProductOrder.objects.create(order=order, title=item.product.title, slug=item.product.slug,
                                        price=item.product.get_price(), quantity=item.quantity,
                                        total_price=item.get_total_price,
                                        photo=image.photo.name if image else '')

        self.clear_basket(minus_quantity=True)

    def clear_basket(self, minus_quantity=False):
        basket_products = self.customer_basket()['products']
        for item in basket_products:
            if minus_quantity:
                item.product.quantity -= item.quantity
                item.product.save()
            item.delete()
