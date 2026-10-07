from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SaleForm, VehicleForm
from .models import Vehicle,Sale


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def vehicle_list(request: HttpRequest) -> HttpResponse:
    vehicles = Vehicle.objects.filter(is_sold=False).order_by("model_name", "registration_number")
    query = request.GET.get("q", "").strip()
    if query:
        from django.db.models import Q
        vehicles = vehicles.filter(Q(model_name__icontains=query) | Q(registration_number__icontains=query))
    return render(request, "vehicle_list.html", {"vehicles": vehicles, "query": query})


def add_vehicle(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "add_vehicle.html")

    form = VehicleForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    vehicle = form.save()
    return JsonResponse({
        "message": "Vehicle added successfully.",
        "vehicle": {
            "vehicle_type": vehicle.get_vehicle_type_display(),
            "model_name": vehicle.model_name,
            "registration_number": vehicle.registration_number,
            "fuel_type": vehicle.get_fuel_type_display(),
            "price": str(vehicle.price),
            "picture_url": vehicle.picture.url if vehicle.picture else "",
        },
    })


def edit_vehicle(request: HttpRequest, id: int) -> HttpResponse:
    vehicle = get_object_or_404(Vehicle, pk=id, is_sold=False)
    form = VehicleForm(request.POST or None, request.FILES or None, instance=vehicle)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if request.method == "POST":
        if form.is_valid():
            vehicle = form.save()
            if is_ajax:
                return JsonResponse({"message": "Vehicle updated successfully.", "vehicle": {
                    "id": vehicle.pk, "vehicle_type": vehicle.get_vehicle_type_display(),
                    "model_name": vehicle.model_name, "registration_number": vehicle.registration_number,
                    "fuel_type": vehicle.get_fuel_type_display(), "price": str(vehicle.price),
                    "picture_url": vehicle.picture.url if vehicle.picture else "",
                }})
            return redirect("vehicle_list")
        if is_ajax:
            return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
    if is_ajax:
        return render(request, "edit_vehicle_form.html", {"form": form, "vehicle": vehicle})
    return render(request, "edit_vehicle.html", {"form": form, "vehicle": vehicle})


def delete_vehicle(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        vehicle = get_object_or_404(Vehicle, pk=id, is_sold=False)
        vehicle.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"message": "Vehicle deleted successfully."})
    return redirect("vehicle_list")


def sell_vehicle(request: HttpRequest, id: int) -> HttpResponse:
    vehicle = get_object_or_404(Vehicle, pk=id, is_sold=False)
    form = SaleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            updated = Vehicle.objects.filter(pk=vehicle.pk, is_sold=False).update(is_sold=True)
            if updated:
                sale = form.save(commit=False)
                sale.vehicle = vehicle
                sale.sold_price = vehicle.price
                sale.save()
                return redirect("vehicle_list")
        form.add_error(None, "This vehicle has already been sold.")
    return render(request, "sell_vehicle.html", {"vehicle": vehicle, "form": form})

def customer_history(request: HttpRequest) -> HttpResponse:
    sales = Sale.objects.select_related("vehicle").order_by("-sold_at")
    return render(request,"sale_history.html",{"sales":sales})


