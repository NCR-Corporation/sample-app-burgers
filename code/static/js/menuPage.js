function goToItemDetails(id, site, tags, time) {
    document.location.pathname =
        "burger/menu/itemDetails/" +
        id +
        "/" +
        site.toLowerCase() +
        "/" +
        tags +
        "/" +
        time;
}
