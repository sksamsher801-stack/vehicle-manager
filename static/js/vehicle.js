$(function () {
    $(document).on("submit", "#vehicleForm", function (event) {
        event.preventDefault();
        const form = this;
        $.ajax({
            url: $(form).attr("action"), type: "POST", data: new FormData(form),
            processData: false, contentType: false,
            success: function (response) {
                $("#message").text(response.message).removeClass("text-danger").addClass("text-success");
                $("#savedRegistration").text(response.vehicle.registration_number);
                $("#savedModel").text(response.vehicle.model_name);
                $("#savedPrice").text(response.vehicle.price);
                $("#savedVehicleBox").removeClass("d-none");
                form.reset();
            },
            error: function (xhr) { showErrors(xhr, "#message"); }
        });
    });

    $(document).on("click", ".edit-vehicle", function () {
        const url = $(this).data("url");
        $("#editVehicleModalBody").html("<p>Loading…</p>");
        bootstrap.Modal.getOrCreateInstance(document.getElementById("editVehicleModal")).show();
        $.ajax({ url: url, headers: { "X-Requested-With": "XMLHttpRequest" } })
            .done(function (html) { $("#editVehicleModalBody").html(html); })
            .fail(function () { $("#editVehicleModalBody").html('<p class="text-danger">Could not load the vehicle form.</p>'); });
    });

    $(document).on("submit", "#editVehicleForm", function (event) {
        event.preventDefault();
        const form = this;
        $.ajax({
            url: form.action, type: "POST", data: new FormData(form),
            processData: false, contentType: false,
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": $(form).find('[name="csrfmiddlewaretoken"]').val() }
        }).done(function (response) {
            const vehicle = response.vehicle;
            const card = $("#vehicle-" + vehicle.id);
            card.find(".vehicle-model").text(vehicle.model_name);
            card.find(".vehicle-number").text(vehicle.registration_number);
            card.find(".vehicle-type").text(vehicle.vehicle_type);
            card.find(".vehicle-fuel").text(vehicle.fuel_type);
            card.find(".vehicle-price").text(vehicle.price);
            let picture = card.find(".vehicle-picture");
            if (vehicle.picture_url) {
                if (!picture.length) {
                    picture = $("<img>", { class: "card-img-top vehicle-picture", alt: vehicle.model_name })
                        .css({ height: "180px", objectFit: "cover" }).prependTo(card.find(".card"));
                }
                picture.attr("src", vehicle.picture_url + "?t=" + Date.now()).attr("alt", vehicle.model_name);
            } else { picture.remove(); }
            bootstrap.Modal.getInstance(document.getElementById("editVehicleModal")).hide();
            $("#vehicleListMessage").text(response.message).removeClass("text-danger").addClass("text-success");
        }).fail(function (xhr) { showErrors(xhr, "#editVehicleErrors"); });
    });

    $(document).on("submit", ".delete-vehicle-form", function (event) {
        event.preventDefault();
        if (!window.confirm("Delete this vehicle?")) return;
        const form = this;
        $.ajax({
            url: form.action, type: "POST", data: $(form).serialize(),
            headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": $(form).find('[name="csrfmiddlewaretoken"]').val() }
        }).done(function (response) {
            $(form).closest("[id^='vehicle-']").fadeOut(150, function () { $(this).remove(); });
            $("#vehicleListMessage").text(response.message).removeClass("text-danger").addClass("text-success");
        }).fail(function () {
            $("#vehicleListMessage").text("Could not delete this vehicle.").removeClass("text-success").addClass("text-danger");
        });
    });

    function showErrors(xhr, target) {
        const errors = xhr.responseJSON && xhr.responseJSON.errors;
        const messages = [];
        if (errors) Object.values(errors).forEach(function (items) {
            items.forEach(function (item) { messages.push(item.message); });
        });
        $(target).text(messages.join(" ") || "Something went wrong.")
            .removeClass("text-success").addClass("text-danger");
    }
});
