var cartValue = sessionStorage.getItem("Cart");
sessionStorage.setItem("Total", 0);

function getCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function getTotal() {
    return JSON.parse(sessionStorage.getItem("Total"));
}

function checkout() {
    document.location.pathname = "/Peachtree-Burger/confirmation";
}

function increaseQuantity(itemId) {
    let element = document.getElementById("quantity-input-" + itemId);
    if (element.placeholder < 5) {
        element.placeholder++;
        addQuantityToCart(itemId);

        document.getElementById("cart-number").innerHTML =
            parseInt(document.getElementById("cart-number").innerHTML) + 1;
    }
}

function decreaseQuantity(itemId) {
    let element = document.getElementById("quantity-input-" + itemId);
    if (element.placeholder > 1) {
        element.placeholder--;
        removeQuantityFromCart(itemId);

        document.getElementById("cart-number").innerHTML =
            parseInt(document.getElementById("cart-number").innerHTML) - 1;
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function addItemToCart() {
    let cart = getCart();
    let total = getTotal();
    let colNumber = 1;
    let checkNumber = 0;

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
                colNumber: colNumber,
            });
            if (checkNumber == colNumber * 4 - 1) {
                colNumber += 1;
            }
            checkNumber += 1;
        });

    delete menuItem.groupToppings;
    delete menuItem.sharedToppings;
    delete menuItem.uniqueToppings;

    menuItem["toppings"] = toppings;

    cart.push(menuItem);

    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);

    document.getElementById("cart-number").innerHTML = 0;
    for (let i = 0; i < cart.length; i++) {
        document.getElementById("cart-number").innerHTML =
            parseInt(document.getElementById("cart-number").innerHTML) +
            cart[i].quantity;
    }
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

function grabCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function addQuantityToCart(element) {
    var cart = grabCart();
    var id = element - 1;

    if (cart[id].quantity < 5) {
        cart[id].quantity += 1;
    } else {
        if (cart[id].quantity == 5) {
            alert("You have reached the max quantity for orders of this item.");
        }
    }

    sessionStorage.setItem("Cart", JSON.stringify(cart));
}

function removeQuantityFromCart(element) {
    var cart = grabCart();
    var id = element - 1;

    if (cart[id].quantity > 1) {
        cart[id].quantity -= 1;
    } else {
        if (cart[id].quantity == 1) {
            alert("You must click remove to delete this item from the cart.");
        }
    }

    sessionStorage.setItem("Cart", JSON.stringify(cart));
}

/**function displayCart() {
    var lst = document.getElementById("order_table");
    var cart = grabCart();
    if (cart[0].item == "0") {
    } else {
        var tHolder = document.getElementById("total");
        var total = 0.0;

        for (let i = 0; i < cart.length; i++) {
            var btn_add = document.createElement("BUTTON");
            var btn_sub = document.createElement("BUTTON");
            var btn_del = document.createElement("BUTTON");
            btn_add.innerHTML = "+";
            btn_sub.innerHTML = "-";
            btn_del.innerHTML = "x";
            btn_add.setAttribute("class", "round");
            btn_add.setAttribute("id", "add" + cart[i].item);
            btn_del.setAttribute("class", "round");
            btn_del.setAttribute("id", "del");
            btn_sub.setAttribute("class", "round");
            btn_sub.setAttribute("id", "sub" + cart[i].item);
            btn_add.setAttribute("onclick", "editCart()");
            btn_sub.setAttribute("onclick", "editCart()");

            var li = document.createElement("li");
            li.appendChild(btn_del);
            li.appendChild(document.createTextNode(cart[i].item));
            li.appendChild(btn_sub);
            li.appendChild(document.createTextNode(" : " + cart[i].qty));
            li.appendChild(btn_add);

            lst.appendChild(li);
            total = total + cart[i].price * cart[i].qty;
            tHolder.innerHTML = total;
        }
    }
}

function editCart() {
    var cart = grabCart();
    var id = parseString(event.srcElement.id);

    for (let i = 0; i < cart.length; i++) {
        if (cart[i].item === id) {
            if (event.srcElement.id.substr(0, 3) === "add") {
                cart[i].qty += 1;
                break;
            } else {
                if (cart[i].qty == 0) {
                    alert("You already have 0 of this item");
                    break;
                } else {
                    cart[i].qty -= 1;
                    break;
                }
            }
        }
    }

    sessionStorage.setItem("Cart", JSON.stringify(cart));

    displayCart();
}

function parseString(id) {
    return id.substr(3);
}

displayCart();
$(document).ready(function () {
    var userCart = grabCart();
    userCart = JSON.stringify({ cart: userCart });

    $("#Checkout").click(function () {
        $.ajax({
            url: "/burger/confirmation",
            headers: {
                "X-CSRFToken": "{{csrf_token}}",
            },
            type: "POST",
            data: { cart: userCart },
            success: function (response) {
                //alert(" I was successful");
            },
            complete: function () {
                window.location.href = "/burger/confirmation";
            },
            error: function (xhr, textStatus, thrownError) {
                alert(
                    "Could not send URL to Django. Error: " +
                        xhr.status +
                        ": " +
                        xhr.responseText
                );
            },
        });
    });
});**/
