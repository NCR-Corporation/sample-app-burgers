sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
sessionStorage.setItem("Copy-Total", JSON.stringify([]));
sessionStorage.setItem("removedItemId", JSON.stringify([]));

function grabCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload();
    }
};
