from django.middleware.common import CommonMiddleware


class ValidateHostMiddleware(CommonMiddleware):
    def process_request(self, request):
        request.get_host()
        return super().process_request(request)
