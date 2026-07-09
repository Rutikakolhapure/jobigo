from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
# We will register a base route for messages

urlpatterns = router.urls
urlpatterns += [
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'mark_read'})),
]
