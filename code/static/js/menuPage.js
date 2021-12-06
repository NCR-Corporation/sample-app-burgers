sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
sessionStorage.setItem("Copy-Total", JSON.stringify([]));
sessionStorage.setItem("removedItemId", JSON.stringify([]));

function goToItemDetails(id, tags) {
    document.location.pathname =
        "Peachtree-Burger/Menu/ItemDetails/" + id + "/" + tags;
}
