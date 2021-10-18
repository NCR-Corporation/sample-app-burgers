function setToLunch(site) {
    sessionStorage.setItem("time", "Lunch");
    document.location.pathname =
        "Peachtree-Burger/Menu/" +
        sessionStorage.getItem("Location").trim() +
        "/Lunch";
}

function setToDinner(site) {
    sessionStorage.setItem("time", "Dinner");
    document.location.pathname =
        "Peachtree-Burger/Menu/" +
        sessionStorage.getItem("Location").trim() +
        "/Dinner";
}

$("#menu").click(function () {
    var site = "midtown";
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        type: "POST",
        url: "/Peachtree-Burger/location",
        headers: { "X-CSRFToken": csrftoken },
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify({ Site: site }),
        success: function (data) {},
        complete: function () {
            window.location.href = "/burger/menu";
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
