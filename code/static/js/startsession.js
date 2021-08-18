var lunchButton = document.getElementById("lunch-menu");
var dinnerButton = document.getElementById("dinner-menu");
var itemNumber = 0;

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

lunchButton.onclick = function () {
    document.location.href = "/";
    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");
};

dinnerButton.onclick = function () {
    document.location.href = "/";
    document.getElementById("store-location").innerHTML =
        sessionStorage.getItem("Location");
};

function locationChange(data) {
    if (sessionStorage.getItem("Location") === null) {
        sessionStorage.setItem("Location", data);

        document.location.href = "/";

        document.getElementById("store-location").innerHTML =
            sessionStorage.getItem("Location");
    } else {
        sessionStorage.setItem("Location", data);

        document.location.href = "/";

        document.getElementById("store-location").innerHTML =
            sessionStorage.getItem("Location");
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
