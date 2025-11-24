from rest_framework.routers import DefaultRouter
from .views import SiteViewSet, LinkViewSet
router = DefaultRouter()
router.register(r"sites", SiteViewSet)
router.register(r"links", LinkViewSet)
urlpatterns = router.urls
