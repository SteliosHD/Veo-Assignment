from typing import List
from veo_company_structure.models import Node
from veo_company_structure.type_hints import json_tree_type, json_dict_tree_type


def get_tree(nodes: List[json_tree_type] = None, root: Node = None) -> json_tree_type:
    if nodes is None:
        nodes = get_dict_nodes()
    if root is None:
        root = get_root()
    dict_tree: json_dict_tree_type = {
        root.id: {'id': root.id, 'parent_id_id': 0, 'name': root.name, 'sub_tree': []}
    }
    # Recursively build the tree from top to bottom
    for node in nodes:
        if not all(key in node for key in ['parent_id_id', 'id', 'name']):
            raise KeyError('The keys "parent_id_id", "id" and "name" must be present in the nodes')
        dict_tree.setdefault(node['parent_id_id'], {'sub_tree': []})
        dict_tree.setdefault(node['id'], {'sub_tree': []})
        dict_tree[node['id']].update(node)
        dict_tree[node['parent_id_id']]['sub_tree'].append(dict_tree[node['id']])
    return dict_tree[root.id]


def get_root(model=None) -> Node:
    if model is None:
        model = Node
    return model.objects.get(parent_id=None)


def get_dict_nodes(model=None) -> List[json_tree_type]:
    """
    This function assumes that the root node is the node with id = 1 (or the first node in the database)
    From the returned list the root node is removed
    :param model: Node model
    :return: List of dictionaries
    """
    if model is None:
        model = Node
    nodes = list(model.objects.values('id', 'parent_id_id', 'name'))
    if len(nodes) < 2:
        return []
    return nodes[1:]
