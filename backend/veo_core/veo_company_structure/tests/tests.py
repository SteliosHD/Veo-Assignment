import pprint
import json
from copy import deepcopy
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.test import  APITestCase

from veo_company_structure.api.node import NodeBaseView
from veo_company_structure.models import Node
from veo_company_structure.serializers import NodeCreateRetrieveSerializer
from veo_company_structure.helpers.tree_utils import get_tree


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

    def helper_test_response(self, response, status_code, redirect_url, message):
        response_status_code = response.status_code if 'status_code' in response.__dir__() else None
        response_redirect_url = response.data.get('url')
        response_message = response.data.get('message')
        self.assertEqual(response_status_code, status_code)
        self.assertEqual(response_redirect_url, redirect_url)
        self.assertEqual(response_message, message)


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
    update_parent_scenario_1 = {}
    descendants_scenario_1 = {}

    def test_node_create_view_and_functionality_success(self):
        parent_id = 1
        url = reverse(viewname='get_create_node', kwargs={'pk': parent_id})
        redirect_url = reverse('index')
        data = {'name': 'CMO', 'parent_id': parent_id, 'node_type': 'MANAGER', 'department_name': 'Marketing'}
        object_count = Node.objects.count()
        latest_id = Node.objects.latest('id').id
        response = self.client.post(url, data)
        self.helper_test_response(response, 201, redirect_url, 'Success')
        self.assertEqual(Node.objects.count(), object_count + 1)
        self.assertEqual(Node.objects.get(name='CMO').parent_id.id, parent_id)
        self.assertEqual(Node.objects.latest('id').id, latest_id + 1)

    def test_tree_retrieve_view_success(self):
        url = reverse(viewname='get_tree')
        redirect_url = reverse('index')
        with open('veo_company_structure/tests/test_data/tree_outputs.json') as f:
            test_expected_tree_1 = json.load(f)['trees'][0]
        response = self.client.get(url)
        response_tree = JSONParser().parse(BytesIO(response.data['tree']))
        self.helper_test_response(response, 200, redirect_url, 'Success')
        self.assertDictEqual(response_tree, test_expected_tree_1)

    def test_update_descentants_scenario_1_builder(self):
        self.helper_descendants_scenario_1_builder()
        scenario = self.descendants_scenario_1
        self.assertEqual(scenario['test_node'].name, 'CFO')
        self.assertEqual(scenario['test_node'].parent_id.id, scenario['test_parent_node'].id)
        self.assertEqual(scenario['test_node'].height, scenario['test_node_initial_height'] + 1)
        for child in scenario['node_base'].get_children(scenario['test_node'].id):
            self.assertEqual(child.height, scenario['test_node_initial_height'] + 1)

    def test_update_descentants_funcionality(self):
        self.helper_descendants_scenario_1_builder()
        scenario = self.descendants_scenario_1
        scenario['node_base'].update_descendants_height(scenario['test_node'])
        test_node_new_height = scenario['test_node'].height
        self.assertEqual(test_node_new_height, scenario['test_node_initial_height'] + 1)
        for child in scenario['node_base'].get_children(scenario['test_node'].id):
            self.assertEqual(child.height, test_node_new_height + 1)

    def test_update_parent__view_response_success(self):
        self.helper_update_view_scenario_1_builder()
        scenario = self.update_parent_scenario_1
        redirect_url = reverse('get_tree')
        response = self.client.patch(scenario['url'], scenario['data'])
        self.helper_test_response(response, 200, redirect_url, 'Success')

    def test_update_parent_view_scenario_1_bulider(self):
        self.helper_update_view_scenario_1_builder()
        scenario = self.update_parent_scenario_1
        self.assertEqual(scenario['test_parent_node'].name, 'CFO')
        self.assertEqual(scenario['test_node'].name, 'CTO')

    def test_update_parent_view_functionality_success(self):
        self.helper_update_view_scenario_1_builder()
        scenario = self.update_parent_scenario_1
        response = self.client.patch(scenario['url'], scenario['data'])
        self.assertEqual(response.status_code, 200)
        test_node_updated = Node.objects.get(id=scenario['test_node_id'])
        test_child_node_updated = Node.objects.get(id=scenario['test_child_node'].id)
        self.assertEqual(test_node_updated.parent_id.id, scenario['parent_id'])
        self.assertEqual(test_node_updated.height, scenario['test_node_initial_height'] + scenario['height_diff'])
        self.assertEqual(test_child_node_updated.height,
                         scenario['test_child_node_initial_height'] + scenario['height_diff'])

    def helper_update_view_scenario_1_builder(self):
        """
        Scenario 1: Update parent of a test node that has childer and the new parent has the same height as the node
        """
        scenario = self.update_parent_scenario_1

        # Hardcoded values
        scenario['parent_id'] = 2  # new parent id
        scenario['test_node_id'] = 3
        scenario['data'] = {'parent_id': scenario['parent_id']}  # payload data

        # Nodes
        scenario['test_node'] = Node.objects.get(id=scenario['test_node_id'])
        scenario['test_parent_node'] = Node.objects.get(id=scenario['parent_id'])
        scenario['test_child_node'] = NodeBaseView().get_children(scenario['test_node_id'])[0]
        scenario['url'] = reverse(viewname='update_node', kwargs={'pk': scenario['test_node_id']})  # url

        # Heights
        scenario['test_node_initial_height'] = deepcopy(scenario['test_node'].height)
        scenario['test_child_node_initial_height'] = deepcopy(scenario['test_child_node'].height)
        scenario['test_node_new_height'] = scenario['test_parent_node'].height + 1
        scenario['height_diff'] = scenario['test_node_new_height'] - scenario['test_node_initial_height']

    def helper_descendants_scenario_1_builder(self):
        scenario = self.descendants_scenario_1
        scenario['node_base'] = NodeBaseView()
        scenario['test_node'] = Node.objects.get(id=2)
        scenario['test_node_initial_height'] = deepcopy(scenario['test_node'].height)
        scenario['test_parent_node'] = Node.objects.get(id=3)
        scenario['test_node'].parent_id = scenario['test_parent_node']
        scenario['test_node'].save()
