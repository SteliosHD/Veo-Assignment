from rest_framework import serializers
from .models import Node


class NodeCreateRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name', 'parent_id', 'height', 'node_type', 'department_name', 'language_preference']
        read_only_fields = ['height']


class NodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name', 'parent_id', 'height', 'node_type', 'department_name', 'language_preference']
        read_only_fields = ['id', 'height', 'node_type', 'department_name', 'language_preference', 'name']
