from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from donations.models import DonationFulfillment, DonationRequest, Neighborhood, Location, PickupTime
from donations.serializers import (
    DonationFulfillmentSerializer, DonationRequestPublicSerializer,
    DonationRequestSerializer, NeighborhoodSerializer, LocationSerializer, PickupTimeSerializer
)


class DonationRequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # Limit to unfulfilled requests made within last 10 days
    def get_queryset(self): 
        queryset = DonationRequest.objects.all()
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood is not None:
            queryset = queryset.filter(neighborhood=neighborhood)
        return queryset.filter(
            created__gte=timezone.now() - timedelta(days=10),
            fulfillments__isnull=True
        )

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('item__category__tag', 'item__tag',)

    def get_serializer_class(self):
        if self.action == 'create':
            return DonationRequestSerializer
        else:
            return DonationRequestPublicSerializer


class DonationFulfillmentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DonationFulfillment.objects.all()
    serializer_class = DonationFulfillmentSerializer


class DonationRequestCodeDetailView(generics.RetrieveAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    lookup_field = 'code'

class NeighborhoodViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer

class LocationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = Location.objects.all()
        neighborhood = self.request.query_params.get('neighborhood', None)

        if neighborhood is not None:
            queryset = queryset.filter(neighborhood=neighborhood)
        return queryset

    serializer_class = LocationSerializer
    
class PickupTimeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    
    def get_queryset(self):
        
        queryset = PickupTime.objects.all()
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood is not None:
            queryset = queryset.filter(neighborhood=neighborhood);
        return queryset

    serializer_class = PickupTimeSerializer


