import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name, description):
    """Создает продукт"""
    product = stripe.Product.create(name=name, description=description)
    return product


def create_stripe_price(product_id, amount):
    """Создает цену для продукта"""
    price = stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=int(amount * 100),  # Цена в копейках
    )
    return price


def create_stripe_session(price_id, success_url, cancel_url):
    """Создает сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
