from typing import Union, List, Dict, Any

json_tree_type = Dict[str, Union[int, str, list]]
json_dict_tree_type = Dict[int, json_tree_type]
