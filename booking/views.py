from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Booking
from .rules import exceeds_limit, overlaps


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["room", "start", "end"]

    def validate(self, attrs):
        if attrs["end"] <= attrs["start"]:
            raise serializers.ValidationError({
                "end": "End must be after start."
            })
        return attrs


@api_view(["POST"])
def create_booking(request):
    s = BookingSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    new = s.validated_data
    if exceeds_limit(new["start"], new["end"]):
        return Response({"error": "too long"}, status=status.HTTP_400_BAD_REQUEST)
    for b in Booking.objects.filter(room=new["room"]):
        if overlaps(b.start, b.end, new["start"], new["end"]):
            return Response({"error": "room taken"}, status=status.HTTP_409_CONFLICT)
    s.save()
    return Response(s.data, status=status.HTTP_201_CREATED)
