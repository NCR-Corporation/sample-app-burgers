if (window.location.pathname == "/Peachtree-Burger/") {
    sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
    sessionStorage.setItem("Copy-Total", JSON.stringify([]));
    sessionStorage.setItem("removedItemId", JSON.stringify([]));
}

$(document).ready(function () {
    if (window.location.hash !== "") {
        var hash = window.location.hash;
        removeHash();

        $("html, body").animate(
            {
                scrollTop: $(hash).offset().top,
            },
            150
        );

        return false;
    }
});

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

function goToCartPage() {
    let csrftoken = getCookie("csrftoken");
    var userCart = JSON.stringify(sessionStorage.getItem("Cart"));

    if (csrftoken == null || cart == null) {
        if (userCart == null) {
            cart = [];
            sessionStorage.setItem("Cart", JSON.stringify(cart));
        }
        document.location.pathname = "/Peachtree-Burger/ViewCart";
    } else {
        $.ajax({
            url: "/Peachtree-Burger/ViewCart",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            type: "POST",
            data: { cart: userCart },
            complete: function () {
                window.location.href = "/Peachtree-Burger/ViewCart";
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
    }
}

function getCart() {
    if (cart === "") {
        sessionStorage.setItem(JSON.stringify);
    }
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function removeHash() {
    history.pushState(
        "",
        document.title,
        window.location.pathname + window.location.search
    );
}

$(document).ready(function () {
    $("a").on("click", function (event) {
        if (this.hash !== "") {
            var hash = this.hash;

            $("html, body").animate(
                {
                    scrollTop: $(hash).offset().top,
                },
                150
            );
            return false;
        }
    });
});

if (sessionStorage.getItem("Location") == null) {
    sessionStorage.setItem("Total", 0);
    $("#dynamicModalCenter").modal({
        backdrop: "static",
        keyboard: false,
        show: true,
    });
} else {
    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");
}

function goToLunchMenu() {
    document.location.pathname =
        "Peachtree-Burger/Menu/" +
        sessionStorage.getItem("Location").trim() +
        "/Lunch";
}

function goToDinnerMenu() {
    document.location.pathname =
        "Peachtree-Burger/Menu/" +
        sessionStorage.getItem("Location").trim() +
        "/Dinner";
}

function locationChange(data, time) {
    var regex = "Peachtree Burger ";
    shortName = data.replace(regex, "");

    sessionStorage.setItem("Location", shortName);

    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");

    if (
        document.location.pathname.substring(0, 22) == "/Peachtree-Burger/Menu"
    ) {
        document.location.pathname =
            "Peachtree-Burger/Menu/" + shortName.trim() + "/" + time;
    } else {
        document.location.reload();
    }
}

function loadDynamicModal() {
    $("#dynamicModalCenter").modal("show");
}

if (
    sessionStorage.getItem("Cart") === null ||
    sessionStorage.getItem("Cart") === ""
) {
    document.getElementById("cart-number").innerHTML = 0;
} else {
    var cart = getCart();
    document.getElementById("cart-number").innerHTML = 0;
    for (let i = 0; i < cart.length; i++) {
        document.getElementById("cart-number").innerHTML =
            parseInt(document.getElementById("cart-number").innerHTML) +
            cart[i].quantity;
    }
}
