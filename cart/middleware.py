from django.utils.deprecation import MiddlewareMixin

class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            request.session.create()
        request.cart_id = request.session.session_key

