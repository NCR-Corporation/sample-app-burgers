function grabCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload();
    }
};
