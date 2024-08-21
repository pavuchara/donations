from django.core.cache import cache

from rest_framework.response import Response


class SimpleListCacheMixin:
    def get(self, request, *args, **kwargs):
        all_instances = cache.get(self.instance_cache_key)

        if all_instances:
            queryset = all_instances
        else:
            queryset = self.get_queryset()
            cache.set(self.instance_cache_key, queryset, 60 * 60)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
