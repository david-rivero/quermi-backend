import os
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def create_payment_customer():
    return stripe.Customer.create()
