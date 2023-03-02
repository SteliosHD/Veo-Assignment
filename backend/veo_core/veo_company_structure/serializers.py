from rest_framework import serializers
from .models import Node


class NodeCreateRetrieveSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), required=True)
    class Meta:
        model = Node
        fields = ['id', 'name', 'parent_id', 'height', 'node_type', 'department_name', 'language_preference']
        read_only_fields = ['height']


class NodeUpdateSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), required=True)

    class Meta:
        model = Node
        fields = ['id', 'name', 'parent_id', 'height', 'node_type', 'department_name', 'language_preference']
        read_only_fields = ['id', 'height', 'node_type', 'department_name', 'language_preference', 'name']
