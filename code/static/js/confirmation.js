document.getElementById("cart-number").innerHTML = 0;
sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
sessionStorage.setItem("Copy-Total", JSON.stringify([]));
sessionStorage.setItem("removedItemId", JSON.stringify([]));

function finish() {
    window
        .open(
            "https://developer.ncr.com/portals/dev-portal/getting-started",
            "_blank"
        )
        .focus();
    document.location.pathname = "/Peachtree-Burger/";
}
