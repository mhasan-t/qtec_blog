from rest_framework import viewsets
from silk.profiling.profiler import silk_profile


# This class wraps all the ModelViewSet functions on silky_profile decorator
class SilkyModelViewset(viewsets.ModelViewSet):
    view_name = ""

    @silk_profile(name=f'list_{view_name}')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @silk_profile(name=f'retrieve_{view_name}')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @silk_profile(name=f'create_{view_name}')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @silk_profile(name=f'update_{view_name}')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @silk_profile(name=f'partial_update_{view_name}')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @silk_profile(name=f'destroy_{view_name}')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
