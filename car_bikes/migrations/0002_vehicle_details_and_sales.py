from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def populate_registration_numbers(apps, schema_editor):
    Vehicle = apps.get_model("car_bikes", "vehicle")
    alias = schema_editor.connection.alias
    vehicles = list(Vehicle.objects.using(alias).all().order_by("pk"))
    for vehicle in vehicles:
        old_quantity = max(1, vehicle.quantity)
        vehicle.registration_number = f"LEGACY-{vehicle.pk}-1"
        vehicle.save(using=alias, update_fields=["registration_number"])
        for unit_number in range(2, old_quantity + 1):
            Vehicle.objects.using(alias).create(
                vehicle_type=vehicle.vehicle_type,
                model_name=vehicle.model_name,
                registration_number=f"LEGACY-{vehicle.pk}-{unit_number}",
                fuel_type=vehicle.fuel_type,
                quantity=1,
                picture=vehicle.picture,
                price=0,
                is_sold=False,
            )


class Migration(migrations.Migration):
    dependencies = [("car_bikes", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="registration_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vehicle",
            name="is_sold",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(populate_registration_numbers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="vehicle",
            name="registration_number",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.RemoveField(model_name="vehicle", name="quantity"),
        migrations.CreateModel(
            name="Sale",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120)),
                ("customer_phone", models.CharField(max_length=30)),
                ("customer_address", models.TextField()),
                ("sold_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("sold_at", models.DateTimeField(auto_now_add=True)),
                ("vehicle", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="sale", to="car_bikes.vehicle")),
            ],
        ),
    ]
