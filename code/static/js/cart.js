var cartValue = sessionStorage.getItem("Cart");
sessionStorage.setItem("Total", 0);

function getCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function getTotal() {
    return JSON.parse(sessionStorage.getItem("Total"));
}

function addItemToCart() {
    let cart = getCart();
    let total = getTotal();
    if (!cart) {
        cart = [];
    }
    let menuItem = JSON.parse(document.getElementById("item").textContent);
    total += menuItem.price;
    let toppings = [];
    $("#item-uniqueToppings--list")
        .children()
        .each((index, item) => {
            total += +item.dataset.itemPrice;
            toppings.push({
                displayName: item.dataset.displayName,
                price: item.dataset.itemPrice,
            });
        });
    delete menuItem.groupToppings;
    delete menuItem.sharedToppings;
    delete menuItem.uniqueToppings;
    menuItem["toppings"] = toppings;
    cart.push(menuItem);
    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);
    console.log(getTotal());
    document.getElementById("cart-number").innerHTML = cart.length;
}

function deleteItem(item) {
    let cart = grabCart();
    var row = item.parentNode.parentNode.rowIndex;
    var itemId = parseString(event.srcElement.id);
    var total = parseFloat(document.getElementById("total").innerHTML);
    var tHolder = document.getElementById("total");

    for (let i = 0; i < cart.length; i++) {
        if (cart[i].item === itemId) {
            total = total - cart[i].price * cart[i].qty;
            tHolder.innerHTML = total;
            cart.splice(i, 1);
            break;
        }
    }

    itemNumber = 0;
    for (var j = 0; j < cart.length; j++) {
        itemNumber = itemNumber + cart[j].qty;
    }

    document.getElementById("cart-number").innerHTML = itemNumber;

    document.getElementById("order_table").deleteRow(row);

    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);
}
