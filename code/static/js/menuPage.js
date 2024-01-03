sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
sessionStorage.setItem("Copy-Total", JSON.stringify([]));
sessionStorage.setItem("removedItemId", JSON.stringify([]));

function goToItemDetails(id, tags) {
    console.log("GoToItemDetails")
    document.location.pathname =
        "Peachtree-Burger/Menu/ItemDetails/" + id + "/" + tags;
}
