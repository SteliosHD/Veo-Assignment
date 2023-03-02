import json
import django

django.setup()

from veo_company_structure.serializers import NodeCreateRetrieveSerializer


def populate_with_data():
    data = json.loads(open('../../veo_company_structure/tests/test_data/tree_inputs.json').read())
    tree = data[0]['data']
    for node in tree:
        serializer = NodeCreateRetrieveSerializer(data=node)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)


if __name__ == '__main__':
    populate_with_data()
