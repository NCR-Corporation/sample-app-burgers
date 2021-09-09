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
    var regex = "Peachtree Burger ";
    shortName = data.replace(regex, "");
    if (sessionStorage.getItem("Location") === null) {
        sessionStorage.setItem("Location", shortName);

        document.location.href = "/";

        document.getElementById("store-location").innerHTML =
            sessionStorage.getItem("Location");
    } else {
        sessionStorage.setItem("Location", shortName);

        document.location.href = "/";

        document.getElementById("store-location").innerHTML =
            sessionStorage.getItem("Location");
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
