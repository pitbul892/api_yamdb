from rest_framework import filters, mixins, viewsets


class MixinViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Name filter mixin."""

    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
