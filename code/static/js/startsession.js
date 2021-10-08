var itemNumber = 0;

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
        "Peachtree-Burger/menu/" +
        sessionStorage.getItem("Location").trim() +
        "/Lunch";
}

function goToDinnerMenu() {
    document.location.pathname =
        "Peachtree-Burger/menu/" +
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
        document.location.pathname.substring(0, 12) == "/Peachtree-Burger/menu"
    ) {
        document.location.pathname =
            "Peachtree-Burger/menu/" + shortName.trim() + "/" + time;
    } else {
        document.location.reload();
    }
}

function loadDynamicModal() {
    $("#dynamicModalCenter").modal("show");
}

if (sessionStorage.getItem("Cart") === null) {
    document.getElementById("cart-number").innerHTML = 0;
} else {
    var cart = getCart();
    document.getElementById("cart-number").innerHTML = cart.length;
}
