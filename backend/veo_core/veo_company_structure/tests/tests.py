import pprint
import json
from django.test import TestCase
from veo_company_structure.models import Node
from veo_company_structure.serializers import NodeSerializer
from veo_company_structure.helpers.tree_utils import get_tree


class TestNodeModel(TestCase):

    def setUp(self) -> None:
        data = json.loads(open('veo_company_structure/tests/test_data/tree_inputs.json').read())
        tree = data[0]['data']
        for node in tree:
            serializer = NodeSerializer(data=node)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)

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
