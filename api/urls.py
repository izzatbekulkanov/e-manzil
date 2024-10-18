from rest_framework_simplejwt.views import TokenBlacklistView
from django.urls import path

from api.apps_api.data_hemis import UpdateUniversityView, SaveHemisKeyView, UniversityWithApiTokenView, \
    delete_university_api_token, SetUniversityActiveView, DataFetchAndSaveView, UniversityDataView
from api.apps_api.e_manzil import DormitoryAddressList, add_dormitory_address, DormitoryAddressDeleteView, \
    AddBuildingView, BuildingFloorDataView, AddFloorView, FloorRoomsView, DeleteFloorView, DeleteBuildingView

data = [
    # boshqa yo'riqnomalar
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('update/university', UpdateUniversityView.as_view(), name='update-university'),
    path('save/hemis/key', SaveHemisKeyView.as_view(), name='save-hemis'),
    path('university/api/list', UniversityWithApiTokenView.as_view(), name='api-token-university'),
    path('delete/university/api/token/', delete_university_api_token, name='delete-university-api-token'),
    path('set-university-active/', SetUniversityActiveView.as_view(), name='set-university-active'),
    path('data/fetch/and/save/', DataFetchAndSaveView.as_view(), name='data-fetch-and-save'),
    path('data/university/statistics/', UniversityDataView.as_view(), name='university-data-view'),
]

e_manzil = [
    path('dormitory-address/', DormitoryAddressList.as_view(), name='dormitory-address-list'),
    path('add-dormitory-address/', add_dormitory_address, name='add-dormitory-address'),
    path('dormitory-address/<int:id>/', DormitoryAddressDeleteView.as_view(), name='delete_dormitory_address'),


    path('add-buildings/', AddBuildingView.as_view(), name='add-building'),
    path('delete-buildings/', DeleteBuildingView.as_view(), name='delete-building'),
    path('building-floor-data/', BuildingFloorDataView.as_view(), name='building-floor-data'),

    path('add-floor/', AddFloorView.as_view(), name='add_new_floor'),
    path('delete-floor/', DeleteFloorView.as_view(), name='delete_floor'),
    path('floor-rooms/<int:floor_id>/', FloorRoomsView.as_view(), name='floor-rooms'),

]

urlpatterns = data + e_manzil
