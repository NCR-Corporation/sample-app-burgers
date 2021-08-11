let map
 
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: new google.maps.LatLng(33.777714, -84.38879),
    zoom: 12,
  });
  const icons = {
    store: {
      icon: "../static/images/Location-Tooltip.svg",
    }
  };
  const features = [
    {
      position: new google.maps.LatLng(33.777714, -84.38879),
      type: "store",
    },
    {
      position: new google.maps.LatLng(33.766137, -84.337588),
      type: "store",
    },
    {
      position: new google.maps.LatLng(33.735645, -84.370725),
      type: "store",
    }
  ];

  // Create markers.
  for (let i = 0; i < features.length; i++) {
    const marker = new google.maps.Marker({
      position: features[i].position,
      icon: icons[features[i].type].icon,
      map: map,
    });
  }
}


$(document).ready(function () {
  $('input[rel="inputAddress"]').popover();
});

var invalidClassName = "invalid";
var inputs = document.querySelectorAll("input, select, textarea");
inputs.forEach(function (input) {
  // Add a css class on submit when the input is invalid.
  input.addEventListener("invalid", function () {
    input.classList.add(invalidClassName);
  });

  // Remove the class when the input becomes valid.
  // 'input' will fire each time the user types
  input.addEventListener("input", function () {
    if (input.validity.valid) {
      input.classList.remove(invalidClassName);
    }
  });
});

$(document).ready(function(){
    

    $("#menu").click(function(){
        var site = "southland"
        $.ajax({
            type:"POST",
            url:'/burger/location',
            headers:{"X-CSRFToken": "{{csrf_token}}"},
            contentType:"application/json;charset=utf-8",
            data: JSON.stringify({'Site':site}),
            success:function(data){
                console.log(data);

            },
            complete:function(){
                window.location.href = "/burger";
            },
            error:function (xhr, textStatus, thrownError){
                alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
            }
        });
    });
});

