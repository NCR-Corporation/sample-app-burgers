if (window.location.pathname == "/Peachtree-Burger/") {
    sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
    sessionStorage.setItem("Copy-Total", JSON.stringify([]));
    sessionStorage.setItem("removedItemId", JSON.stringify([]));
}

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
    var regex = "Peachtree Burger ";
    shortName = data.replace(regex, "");
    sessionStorage.setItem("Location", shortName);
    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");

    var time = new Date();
    if (time.getHours() < 14) {
        document.location.pathname =
            "Peachtree-Burger/Menu/" + shortName.trim() + "/Lunch";
    } else {
        document.location.pathname =
            "Peachtree-Burger/Menu/" + shortName.trim() + "/Dinner";
    }
}
