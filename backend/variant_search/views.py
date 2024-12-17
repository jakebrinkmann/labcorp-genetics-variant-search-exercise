from typing import TYPE_CHECKING

from variant_search.models import Variant
from rest_framework import pagination, viewsets, filters
from variant_search.serializers import GeneSerializer, VariantSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet


def publish_to_kafka(pk):
    print(f"Publishing {pk} to Kafka")


class VariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows queries to fetch Variant data.
    """

    # The variable must be named queryset
    # Filter out rows with a blank gene
    # Apply and then filter by the gene param if set
    queryset = Variant.objects.exclude(gene="")
    serializer_class = VariantSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("gene",)

    def update(self, request, pk=None):
        """I want to be able to update properties on an existing variant
        by calling an endpoint.

        The change should then be published as an event to Kafka."""
        variant = Variant.objects.get(pk)
        publish_to_kafka(pk)
        variant.update(**request.json)
        variant.save()


class GeneViewSetPagination(pagination.PageNumberPagination):
    # Return a lot more gene values, since they are small
    page_size = 100


class GeneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the gene autosuggest feature
    """

    # The variable must be named queryset
    # Filter out rows with a blank gene
    # Apply and then filter by the gene param if set
    queryset = Variant.objects.exclude(gene="").values("gene").distinct()
    serializer_class = GeneSerializer
    # Return a lot more gene values, since they are small
    pagination_class = GeneViewSetPagination

    def get_queryset(self) -> "QuerySet":
        """
        Filter by the gene param if set
        """
        gene_suggest = self.request.query_params.get("geneSuggest", "").strip()
        return (
            self.queryset.filter(gene__contains=gene_suggest.upper())
            if gene_suggest
            else self.queryset
        )
