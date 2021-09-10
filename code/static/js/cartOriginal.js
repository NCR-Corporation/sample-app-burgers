var cartValue = sessionStorage.getItem("Cart");

function grabCart() {
    var cart = sessionStorage.getItem("Cart");
    return JSON.parse(cart);
}

function displayCart() {
    var lst = document.getElementById("order_list");
    var cart = grabCart();
    if (cart[0].item == "0") {
    } else {
        var tHolder = document.getElementById("total");
        var total = 0.0;
        lst.innerHTML = "";

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
