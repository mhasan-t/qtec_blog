from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from silk.profiling.profiler import silk_profile


# This func returns a class wraps all the ModelViewSet functions on silky_profile decorator
# view_name param is for the Silk ui.
# This will cache the GET requests for 2 hours.
# POST/PUT/DELETE will invalidate the cache as it updates the database.
def GetBaseModelViewSet(view_name):
    class BaseModelViewSet(viewsets.ModelViewSet):
        @silk_profile(name=f'list_{view_name}')
        @method_decorator(cache_page(60 * 60 * 2))
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

        @silk_profile(name=f'retrieve_{view_name}')
        @method_decorator(cache_page(60 * 60 * 2))
        def retrieve(self, request, *args, **kwargs):
            return super().retrieve(request, *args, **kwargs)

        @silk_profile(name=f'create_{view_name}')
        def create(self, request, *args, **kwargs):
            cache.clear()
            return super().create(request, *args, **kwargs)

        @silk_profile(name=f'update_{view_name}')
        def update(self, request, *args, **kwargs):
            cache.clear()
            return super().update(request, *args, **kwargs)

        @silk_profile(name=f'partial_update_{view_name}')
        def partial_update(self, request, *args, **kwargs):
            cache.clear()
            return super().partial_update(request, *args, **kwargs)

        @silk_profile(name=f'destroy_{view_name}')
        def destroy(self, request, *args, **kwargs):
            cache.clear()
            return super().destroy(request, *args, **kwargs)

    return BaseModelViewSet
