from django.utils.deprecation import MiddlewareMixin

class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ensure a session exists
        if not request.session.session_key:
            request.session.create()

        # Use session key as the cart identifier
        request.cart_id = request.session.session_key
