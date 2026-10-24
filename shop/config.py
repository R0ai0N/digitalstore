def filter_products(request, products):
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    if brand:
        products = products.filter(brand__slug=brand)

    if model:
        products = products.filter(model__slug=model)

    if price_from and price_from.isdigit():
        products = products.filter(price__gte=price_from)

    if price_to and price_to.isdigit():
        products = products.filter(price__lte=price_to)

    return products
