from rest_framework import serializers

from .models import Turn, Order, TurnSubmission


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = "__all__"
        read_only_fields = [f.name for f in Turn._meta.get_fields() if hasattr(f, "name")]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.Serializer):
    order_type = serializers.ChoiceField(choices=Order.OrderType.choices)
    payload = serializers.JSONField(default=dict)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data


class TurnSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnSubmission
        fields = "__all__"
        read_only_fields = [f.name for f in TurnSubmission._meta.get_fields() if hasattr(f, "name")]
