from typing import Union, Dict

json_tree_type = Dict[str, Union[int, str, list]]
json_dict_tree_type = Dict[int, json_tree_type]
