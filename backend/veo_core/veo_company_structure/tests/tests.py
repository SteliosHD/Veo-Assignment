import pprint
import json
from copy import deepcopy
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.test import APIRequestFactory, APITestCase

from veo_company_structure.api.node import NodeBaseView
from veo_company_structure.models import Node
from veo_company_structure.serializers import NodeCreateRetrieveSerializer
from veo_company_structure.helpers.tree_utils import get_tree
from veo_company_structure.urls import API_URL


class TestBase(TestCase):
    def setUp(self) -> None:
        data = json.loads(open('veo_company_structure/tests/test_data/tree_inputs.json').read())
        tree = data[0]['data']
        for node in tree:
            serializer = NodeCreateRetrieveSerializer(data=node)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)


class TestNodeModel(TestBase):

    def test_node_model_creation(self):
        root_node = Node.objects.get(id=1)
        self.assertEqual(root_node.name, 'CEO')
        self.assertEqual(root_node.parent_id, None)
        self.assertEqual(root_node.height, 0)
        self.assertEqual(root_node.node_type, 'MANAGER')
        cfo_node = Node.objects.get(name='CFO')
        self.assertEqual(cfo_node.id, 2)
        self.assertEqual(cfo_node.parent_id.id, 1)
        self.assertEqual(cfo_node.height, 1)
        self.assertEqual(cfo_node.node_type, 'MANAGER')

    def test_tree_parser(self):
        test_tree_1 = get_tree()
        with open('veo_company_structure/tests/test_data/tree_outputs.json') as f:
            test_expected_tree_1 = json.load(f)['trees'][0]
        self.assertEqual(pprint.pformat(test_tree_1), pprint.pformat(test_expected_tree_1))
        self.assertDictEqual(test_tree_1, test_expected_tree_1)


class TestNodeViews(TestBase, APITestCase):

    def test_node_create(self):
        # TODO: Break this test into smaller tests
        parent_id = 1
        url = reverse(viewname='get_create_node', kwargs={'pk': parent_id})
        redirect_url = reverse('index')
        data = {'name': 'CMO', 'parent_id': parent_id, 'node_type': 'MANAGER', 'department_name': 'Marketing'}
        object_count = Node.objects.count()
        latest_id = Node.objects.latest('id').id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Node.objects.count(), object_count + 1)
        self.assertEqual(Node.objects.get(name='CMO').parent_id.id, parent_id)
        self.assertEqual(response.data['url'], redirect_url)
        self.assertEqual(response.data['message'], 'Node created successfully')
        self.assertEqual(Node.objects.latest('id').id, latest_id + 1)

    def test_tree_retrieve_view_success(self):
        url = reverse(viewname='get_tree')
        with open('veo_company_structure/tests/test_data/tree_outputs.json') as f:
            test_expected_tree_1 = json.load(f)['trees'][0]
        response = self.client.get(url)
        response_tree = JSONParser().parse(BytesIO(response.data['tree']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Success')
        self.assertDictEqual(response_tree, test_expected_tree_1)

    def test_update_descentant(self):
        node_base = NodeBaseView()
        test_node = Node.objects.get(id=2)
        test_node_initial_height = deepcopy(test_node.height)
        self.assertEqual(test_node.name, 'CFO')
        test_parent_node = Node.objects.get(id=3)
        test_node.parent_id = test_parent_node
        test_node.save()
        self.assertEqual(test_node.parent_id.id, test_parent_node.id)
        self.assertEqual(test_node.height, test_node_initial_height + 1)
        for child in node_base.get_children(test_node.id):
            self.assertEqual(child.height, test_node_initial_height + 1)
        node_base.update_descendants_height(test_node)
        test_node_new_height = test_node.height
        self.assertEqual(test_node_new_height, test_node_initial_height + 1)

        for child in node_base.get_children(test_node.id):
            self.assertEqual(child.height, test_node_new_height + 1)

