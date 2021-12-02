var cartValue = sessionStorage.getItem("Cart");

if (window.location.pathname == "/Peachtree-Burger/ViewCart" && cartValue) {
    sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
    sessionStorage.setItem("Copy-Total", JSON.stringify([]));
    sessionStorage.setItem("removedItemId", JSON.stringify([]));
    setTotalValues();
}

function formatMoney(number) {
    return number.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
    });
}

function grabCart() {
    if (cart === "") {
        sessionStorage.setItem(JSON.stringify);
    }
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function getTotal() {
    return parseFloat(sessionStorage.getItem("Total"));
}

function backToMenu(menuLink) {
    document.location.pathname = menuLink;
}

function checkout() {
    sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
    sessionStorage.setItem("Copy-Total", JSON.stringify([]));
    sessionStorage.setItem("removedItemId", JSON.stringify([]));
    sessionStorage.setItem("Cart", JSON.stringify([]));
    sessionStorage.setItem("Total", 0);
    sessionStorage.setItem("cart-number", 0);

    document.location.pathname = "/Peachtree-Burger/Confirmation";
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
    let cart = grabCart();
    let total = getTotal();
    let colNumber = 1;
    let checkNumber = 0;

    if (!cart) {
        cart = [];
    }

    copyCart = sessionStorage.getItem("Copy-Cart");

    if (sessionStorage.getItem("Copy-Cart") != "[]") {
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

        if (toppings.length) {
            cart[sessionStorage.getItem("removedItemId")].toppings = toppings;
        }
        sessionStorage.setItem("Cart", JSON.stringify(cart));
        sessionStorage.setItem("Copy-Cart", JSON.stringify([]));
        sessionStorage.setItem("Copy-Total", JSON.stringify([]));
        sessionStorage.setItem("removedItemId", JSON.stringify([]));
    } else {
        let menuItem = JSON.parse(document.getElementById("item").textContent);
        total += parseFloat(menuItem.price.substring(1));

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
}

function deleteItem(itemId) {
    let cart = grabCart();
    if (!cart) {
        cart = [];
    }

    total =
        sessionStorage.getItem("Total") -
        parseFloat(cart[itemId - 1].price.substring(1)) *
            parseFloat(cart[itemId - 1].quantity);
    cart.splice(itemId - 1, 1);
    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);

    let csrftoken = getCookie("csrftoken");
    var userCart = JSON.stringify(sessionStorage.getItem("Cart"));

    if (csrftoken == null || cart == null) {
        if (userCart == null) {
            cart = [];
            sessionStorage.setItem("Cart", JSON.stringify(cart));
        }
        document.location.pathname = "/Peachtree-Burger/ViewCart";
    } else {
        $.ajax({
            url: "/Peachtree-Burger/ViewCart",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            type: "POST",
            data: { cart: userCart },
            complete: function () {
                window.location.href = "/Peachtree-Burger/ViewCart";
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
    }
}

function editCart(itemId) {
    let copyCart = grabCart();

    if (!copyCart) {
        cart = [];
    }

    sessionStorage.setItem("Copy-Cart", JSON.stringify(copyCart));
    sessionStorage.setItem("Copy-Total", total);
    sessionStorage.setItem("removedItemId", itemId - 1);

    document.location.pathname =
        "/Peachtree-Burger/Menu/ItemDetails/" +
        cart[itemId - 1].id +
        "/" +
        cart[itemId - 1].tags[0];
}

function addQuantityToCart(element) {
    var cart = grabCart();
    var id = element - 1;
    let total = getTotal();

    if (cart[id].quantity < 5) {
        cart[id].quantity += 1;
        total += parseFloat(cart[id].price.substring(1));
    } else {
        if (cart[id].quantity == 5) {
            alert("You have reached the max quantity for orders of this item.");
        }
    }

    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);
    setTotalValues();
}

function removeQuantityFromCart(element) {
    var cart = grabCart();
    var id = element - 1;
    let total = getTotal();

    if (cart[id].quantity > 1) {
        cart[id].quantity -= 1;
        total -= parseFloat(cart[id].price.substring(1));
    } else {
        if (cart[id].quantity == 1) {
            alert("You must click remove to delete this item from the cart.");
        }
    }

    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);
    setTotalValues();
}

function setTotalValues() {
    $("#subtotal").html(
        "Subtotal: " + formatMoney(parseFloat(sessionStorage.getItem("Total")))
    );
    $("#tax").html(
        "Georgia Tax(6.0%): " +
            formatMoney(parseFloat(sessionStorage.getItem("Total")) * 0.06)
    );
    $("#total").html(
        "Total: " +
            formatMoney(
                parseFloat(sessionStorage.getItem("Total")) * 0.06 +
                    parseFloat(sessionStorage.getItem("Total"))
            )
    );
}
