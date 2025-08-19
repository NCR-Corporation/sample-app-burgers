document.getElementById("cart-number").innerHTML = 0;
sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
sessionStorage.setItem("Copy-Total", JSON.stringify([]));
sessionStorage.setItem("removedItemId", JSON.stringify([]));

function finish() {
    window
        .open(
            "https://developer.ncrvoyix.com/portals/dev-portal/getting-started",
            "_blank"
        )
        .focus();
    document.location.pathname = "/Peachtree-Burger/";
}
