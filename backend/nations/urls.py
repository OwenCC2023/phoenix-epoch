from django.urls import path

from . import views

urlpatterns = [
    path("", views.NationListCreateView.as_view(), name="nation-list-create"),
    path("<int:pk>/", views.NationDetailView.as_view(), name="nation-detail"),
    path("<int:pk>/resources/", views.NationResourcesView.as_view(), name="nation-resources"),
    path("<int:pk>/provinces/", views.NationProvincesView.as_view(), name="nation-provinces"),
    path("<int:pk>/policies/", views.NationPolicyListView.as_view(), name="nation-policies"),
    path("<int:pk>/military/groups/", views.NationMilitaryGroupsView.as_view(), name="nation-military-groups"),
    path("<int:pk>/military/formations/", views.NationFormationsView.as_view(), name="nation-military-formations"),
]
