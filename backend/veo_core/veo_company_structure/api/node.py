from typing import List

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from veo_company_structure.helpers.tree_utils import get_tree
from veo_company_structure.models import Node
from veo_company_structure.serializers import NodeCreateRetrieveSerializer, NodeUpdateSerializer


class NodeBaseView(generics.GenericAPIView):
    queryset = Node.objects.all()

    def get_queryset(self):
        return Node.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def get_or_create_node_id(self, request):
        if request.data.get('id') is None:
            request.POST._mutable = True
            request.data['id'] = self.queryset.latest('id').id + 1
            request.POST._mutable = False

    def update_descendants_height(self, root_node) -> bool:
        """
        Updates the height of all descendants of a node one by one and save them to the database
        """
        to_be_visited: List[Node] = [root_node]
        while to_be_visited:
            current_node = to_be_visited.pop()
            current_node.height = current_node.parent_id.height + 1 if current_node.parent_id else 0
            current_node.save()
            to_be_visited.extend(self.get_children(current_node))
        return True

    def get_children(self, node_id) -> List[Node]:
        """
        Returns a queryset of children nodes of a node (1 level)
        """
        return list(self.queryset.filter(parent_id=node_id).all())


class CreateRetriveView(generics.CreateAPIView, generics.RetrieveAPIView, NodeBaseView):
    serializer_class = NodeCreateRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        node = self.get_object()
        serializer = self.serializer_class(node)
        return Response(JSONRenderer().render(serializer.data))

    def create(self, request, *args, **kwargs):
        self.get_or_create_node_id(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            url = reverse(viewname='index')
            return Response({'url': url, 'message': 'Node created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class UpdateNodeView(generics.UpdateAPIView, NodeBaseView):
    serializer_class = NodeUpdateSerializer

    def update(self, request, *args, **kwargs):
        node = self.get_object()
        self.get_or_create_node_id(request)
        serializer = self.serializer_class(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.update_descendants_height(node)
            url = reverse(viewname='get_tree')
            data = {'url': url, 'message': 'Node updated successfully'}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class RetrieveChildrenView(generics.RetrieveAPIView, NodeBaseView):
    serializer_class = NodeCreateRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        node = self.get_object()
        children = self.get_children(node.id)
        serializer = self.serializer_class(children, many=True)
        return Response(data=JSONRenderer().render(serializer.data))


class RetrieveTreeJSONView(generics.RetrieveAPIView, NodeBaseView):
    serializer_class = NodeCreateRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        tree = get_tree()
        url_redirect = reverse(viewname='index')
        data = {'tree': JSONRenderer().render(tree), 'url': url_redirect, 'message': 'Success'}
        return Response(data=data, status=status.HTTP_200_OK)
