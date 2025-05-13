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
    var userCart = sessionStorage.getItem("Cart");
    var csrftoken = getCookie("csrftoken");

    $.ajax({
        url: "/Peachtree-Burger/ViewCart",
        headers: {
            "X-CSRFToken": csrftoken,
        },
        type: "POST",
        data: { cart: userCart },
        complete: function () {
            sessionStorage.setItem("Cart", JSON.stringify([]));
            sessionStorage.setItem("Total", 0);
            sessionStorage.setItem("cart-number", 0);

            document.location.pathname = "/Peachtree-Burger/Confirmation";
        },
        error: function (xhr, textStatus, thrownError) {
            alert("Error sending cart: " + xhr.status + ": " + xhr.responseText);
        }
    });
}

function increaseQuantity(index) {
    index = parseInt(index);
    let cart = grabCart();
    const input = document.getElementById("quantity-input-" + index);

    if (cart[index].quantity < 5) {
        cart[index].quantity += 1;
        input.value = cart[index].quantity;

        sessionStorage.setItem("Cart", JSON.stringify(cart));
        updateCartNumber();
        setTotalValues();
    }
}

function decreaseQuantity(index) {
    index = parseInt(index);
    let cart = grabCart();
    const input = document.getElementById("quantity-input-" + index);

    if (cart[index].quantity > 1) {
        cart[index].quantity -= 1;
        input.value = cart[index].quantity;

        sessionStorage.setItem("Cart", JSON.stringify(cart));
        updateCartNumber();
        setTotalValues();
    } else {
        alert("Click remove to delete this item.");
    }
}

function updateCartNumber() {
    const cart = grabCart();
    let totalItems = 0;
    cart.forEach(item => {
        totalItems += item.quantity || 1;
    });
    document.getElementById("cart-number").innerHTML = totalItems;
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
                if (item.dataset.itemPrice === undefined) {
                    return;
                }
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
    if (!cart) cart = [];

    // Find item index by itemId (not assuming position)
    const itemIndex = cart.findIndex(item => item.id === itemId);

    if (itemIndex === -1) {
        alert("Item not found in cart.");
        return;
    }

    const item = cart[itemIndex];
    const itemPrice = parseFloat(item.price.replace('$', ''));
    const itemQuantity = parseInt(item.quantity);

    let total = getTotal();
    total -= itemPrice * itemQuantity;

    cart.splice(itemIndex, 1);  // remove the item
    sessionStorage.setItem("Cart", JSON.stringify(cart));
    sessionStorage.setItem("Total", total);

    const csrftoken = getCookie("csrftoken");
    const userCart = JSON.stringify(cart);

    if (!csrftoken) {
        alert("Missing CSRF token.");
        return;
    }

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
                "Could not send cart to Django. Error: " +
                xhr.status +
                ": " +
                xhr.responseText
            );
        },
    });
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
    const cart = grabCart();
    let subtotal = 0;

    cart.forEach(item => {
        const price = parseFloat(item.price.replace('$', ''));
        const qty = parseInt(item.quantity);
        subtotal += price * qty;
    });

    sessionStorage.setItem("Total", subtotal);

    $("#subtotal").html("Subtotal: " + formatMoney(subtotal));
    $("#tax").html("Georgia Tax(6.0%): " + formatMoney(subtotal * 0.06));
    $("#total").html("Total: " + formatMoney(subtotal * 1.06));
}
