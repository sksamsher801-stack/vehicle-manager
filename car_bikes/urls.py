from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("add-vehicle/", views.add_vehicle, name="add_vehicle"),
    path("vehicles/edit/<int:id>/", views.edit_vehicle, name="edit_vehicle"),
    path("vehicles/delete/<int:id>/", views.delete_vehicle, name="delete_vehicle"),
    path("vehicles/sell/<int:id>/", views.sell_vehicle, name="sell_vehicle"),
    path("customer-history/", views.customer_history, name="customer_history"),
]
