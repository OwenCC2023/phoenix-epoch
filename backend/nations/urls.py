from django.urls import path

from . import views
from provinces import views as province_views

urlpatterns = [
    path("", views.NationListCreateView.as_view(), name="nation-list-create"),
    path("<int:pk>/", views.NationDetailView.as_view(), name="nation-detail"),
    path("<int:pk>/resources/", views.NationResourcesView.as_view(), name="nation-resources"),
    path("<int:pk>/provinces/", views.NationProvincesView.as_view(), name="nation-provinces"),
    path("<int:pk>/policies/", views.NationPolicyListView.as_view(), name="nation-policies"),
    path("<int:pk>/military/groups/", views.NationMilitaryGroupsView.as_view(), name="nation-military-groups"),
    path("<int:pk>/military/formations/", views.NationFormationsView.as_view(), name="nation-military-formations"),
    # Control & Rebellion System — Region endpoints
    path("<int:nation_id>/regions/", province_views.RegionListCreateView.as_view(), name="region-list-create"),
    path("<int:nation_id>/regions/<int:pk>/", province_views.RegionDetailView.as_view(), name="region-detail"),
    path("<int:nation_id>/regions/<int:pk>/add-province/", province_views.RegionAddProvinceView.as_view(), name="region-add-province"),
    path("<int:nation_id>/regions/<int:pk>/remove-province/", province_views.RegionRemoveProvinceView.as_view(), name="region-remove-province"),
    path("<int:nation_id>/rebellions/", province_views.RebellionListView.as_view(), name="nation-rebellions"),
]
