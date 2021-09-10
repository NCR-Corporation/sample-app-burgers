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
        "burger/menu/" + sessionStorage.getItem("Location").trim() + "/Lunch";
}

function goToDinnerMenu() {
    document.location.pathname =
        "burger/menu/" + sessionStorage.getItem("Location").trim() + "/Dinner";
}

function locationChange(data, time) {
    var regex = "Peachtree Burger ";
    shortName = data.replace(regex, "");

    sessionStorage.setItem("Location", shortName);

    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");

    if (document.location.pathname.substring(0, 12) == "/burger/menu") {
        document.location.pathname =
            "burger/menu/" + shortName.trim() + "/" + time;
    } else {
        document.location.reload();
    }
}

function loadDynamicModal() {
    $("#dynamicModalCenter").modal("show");
}

if (sessionStorage.getItem("Cart") === null) {
    sessionStorage.setItem(
        "Cart",
        JSON.stringify([
            {
                item: "0",
                price: 0,
                qty: 0,
            },
        ])
    );
    document.getElementById("cart-number").innerHTML = 0;
} else {
    var cart = grabCart();

    if (cart.length) {
        for (var i = 0; i < cart.length; i++) {
            itemNumber = itemNumber + cart[i].qty;
        }
    }

    document.getElementById("cart-number").innerHTML = itemNumber;
}
