function removeFromUniqueToppings(item, topping) {
    item.groupToppings.pop();
}

let menuItem;

$(function () {
    menuItem = JSON.parse(document.getElementById("item").textContent);
    initialize(menuItem);
});

function initialize(menuItem) {
    const {
        description,
        displayName,
        groupToppings,
        id,
        image,
        price,
        sharedToppings,
        tags,
        uniqueToppings,
    } = menuItem;

    let includedItems = [...uniqueToppings];

    if (includedItems.length) {
        includedItems.forEach((item, index) => {
            createItemCard({
                item,
                included: true,
                container: "#item-uniqueToppings--list",
                type: "uniqueToppings",
            });
        });
        let defaultCard = createDefaultCard();
        $(defaultCard).appendTo("#item-uniqueToppings--list-optional");
    }

    if (sharedToppings.length) {
        sharedToppings.forEach((item, index) => {
            createItemCard({
                item,
                included: false,
                container: "#item-sharedToppings--list-optional",
                type: "sharedToppings",
            });
        });
    }

    if (groupToppings.length) {
        groupToppings.forEach((item, index) => {
            createItemCard({
                item,
                included: false,
                container: "#item-groupToppings--list-optional",
                type: "groupToppings",
            });
        });
    }
}

function createDefaultCard(text = "No other available toppings") {
    return `<div class='col-4 col-md-3 col-lg-2 my-2' data-display-name="default">
        <div class="card shadow-sm">
            <div class="card-body">
                <p class="text-center mb-0">${text}</p>
            </div>
        </div>
    </div>`;
}

function createItemCard({ item, included, container, type }) {
    price = item.price.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
    });

    $(`<div class='col-4 col-md-3 col-lg-2 my-2' data-display-name="${
        item.displayName
    }" data-item-price="${item.price}">
        <div class='card shadow-sm h-100'>
            <div class='d-flex justify-content-end pt-1' onclick='removeItem({ displayName: "${
                item.displayName
            }", container: "${container}", type: "${type}" })'>
                <span class='fa-stack fa-lg'>
                    <i class='fas fa-circle fa-stack-2x' style='${
                        included ? "color: #ff3b30" : "color: #54b948"
                    }'></i>
                    <i class="fas ${
                        included ? "fa-minus" : "fa-plus"
                    } fa-stack-1x" style="color: white; font-size: 1em"></i>
                </span>
            </div>
            <div class='card-body py-0'>
                <img src="${
                    item.image
                }" class="card-img-top my-1" style="object-fit: cover; max-height: 150px; min-height:150px"/>
                <p class="h5 text-center">${item.displayName}</p>
                <p class="h6 text-center">${price}</p>
                
            </div>
        </div>
    </div>`).appendTo(container);
}

function removeItem({ displayName, container, type }) {
    $(container)
        .children()
        .filter((index, element) => element.dataset.displayName === displayName)
        .remove();
    if (!container.includes("optional")) {
        let changedItem = menuItem[type].filter((element) => {
            return element.displayName === displayName;
        })[0];
        if (
            $(`#item-${type}--list-optional`).children()[0].dataset
                .displayName === "default"
        ) {
            $(`#item-${type}--list-optional`).children().first().remove();
        }
        createItemCard({
            item: changedItem,
            included: false,
            container: `#item-${type}--list-optional`,
            type,
        });
    } else {
        let changedItem = menuItem[type].filter((element) => {
            return element.displayName === displayName;
        })[0];
        if (
            $(`#item-uniqueToppings--list`).children()[0].dataset
                .displayName === "default"
        ) {
            $(`#item-uniqueToppings--list`).children().first().remove();
        }
        createItemCard({
            item: changedItem,
            included: true,
            container: `#item-uniqueToppings--list`,
            type,
        });
    }
    if ($(container).children().length === 0) {
        if (container === "#item-uniqueToppings--list") {
            let defaultCard = createDefaultCard("No toppings");
            $(defaultCard).appendTo(container);
        } else {
            let defaultCard = createDefaultCard();
            $(defaultCard).appendTo(container);
        }
    }
}
