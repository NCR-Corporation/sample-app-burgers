var lunchButton = document.getElementById('lunch-menu');
var dinnerButton = document.getElementById('dinner-menu');
var itemNumber = 0;

lunchButton.onclick = function(){
    location.assign('/');
}

dinnerButton.onclick = function(){
    location.assign('/');
}

if (sessionStorage.getItem("Cart") === null){
    sessionStorage.setItem('Cart', JSON.stringify([{
                                        item: '0',
                                        price: 0,
                                        qty: 0,
                                   }]));
    document.getElementById('cart-number').innerHTML = 0;
}
else{

    var cart = grabCart();

    if(cart.length){
        for(var i = 0; i < cart.length; i++){
            itemNumber = itemNumber + cart[i].qty;
        }
    }

    document.getElementById('cart-number').innerHTML = itemNumber;  
}