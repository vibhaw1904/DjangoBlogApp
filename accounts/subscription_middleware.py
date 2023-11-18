from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import UserSubscription

# class SubscriptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             try:
#                 subscription = UserSubscription.objects.get(user=request.user)
#                 if subscription.expired_at > timezone.now():
#                     return self.get_response(request)
#             except UserSubscription.DoesNotExist:
#                 pass
#             return HttpResponseForbidden("Subscription required for this action.")
#         return self.get_response(request)
