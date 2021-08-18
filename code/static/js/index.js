let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(33.777714, -84.38879),
        zoom: 12,
    });
    const icons = {
        store: {
            icon: "../static/images/Location-Tooltip.svg",
        },
    };
    const features = [
        {
            position: new google.maps.LatLng(33.777714, -84.38879),
            type: "store",
        },
        {
            position: new google.maps.LatLng(33.766137, -84.337588),
            type: "store",
        },
        {
            position: new google.maps.LatLng(33.735645, -84.370725),
            type: "store",
        },
    ];

    // Create markers.
    for (let i = 0; i < features.length; i++) {
        const marker = new google.maps.Marker({
            position: features[i].position,
            icon: icons[features[i].type].icon,
            map: map,
        });
    }
}

function setLocation(data) {
    console.log(data);
    var regex = "Peachtree Burger ";
    shortName = data.replace(regex, "");
    sessionStorage.setItem("Location", shortName);
    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $("#menu").click(function () {
        var site = "midtown";
        var csrftoken = getCookie("csrftoken");
        $.ajax({
            type: "POST",
            url: "/burger/location",
            headers: { "X-CSRFToken": csrftoken },
            contentType: "application/json;charset=utf-8",
            data: JSON.stringify({ Site: site }),
            success: function (data) {},
            complete: function () {
                window.location.href = "/burger/menu";
            },
            error: function (xhr, textStatus, thrownError) {
                alert(
                    "Could not send URL to Django. Error: " +
                        xhr.status +
                        ": " +
                        xhr.responseText
                );
            },
        });
    });
});
