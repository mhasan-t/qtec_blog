from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryViews)
router.register(r'blogs', views.BlogViews)
router.register(r'posts', views.PostViews)

urlpatterns = router.urls
