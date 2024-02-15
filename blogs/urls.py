from rest_framework import routers

from . import views

app_name = 'blogs'

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryViews)
router.register(r'posts', views.PostViews)
router.register(r'', views.BlogViews)

urlpatterns = router.urls
