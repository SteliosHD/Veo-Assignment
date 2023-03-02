from django.urls import path
from veo_company_structure import views
from veo_company_structure.api import node

API_URL = 'api/v1/'

urlpatterns = [
    path("index", views.index, name="index"),
    path("nodes/<pk>", node.CreateRetrieveView.as_view(), name="get_create_node"),
    path("nodes/<pk>/update", node.UpdateNodeView.as_view(), name="update_node"),
    path("tree", node.RetrieveTreeJSONView.as_view(), name="get_tree"),
]
