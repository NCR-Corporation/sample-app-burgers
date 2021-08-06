var cartValue = sessionStorage.getItem('Cart');
sessionStorage.setItem('Total',0);

function grabCart(){
    var cart = sessionStorage.getItem("Cart")
    return JSON.parse(cart);
}

function parseString(id){

return id.substr(3);
}

function displayCart(){

    var lst = document.getElementById("order_table");
    var cart = grabCart();
    if(cart[0].item == '0'){

    }else{
         var tHolder = document.getElementById('total');
         var total = 0.0;
         lst.innerHTML = "";


         var heading = document.createElement("TR");

         var h1 = document.createElement('th');

         heading.appendChild(h1);

         var h2 = document.createElement('th');

         h2.innerHTML = "Item Name";
         h2.className = "text-center";
         heading.appendChild(h2);

         var h3 = document.createElement('th');
         heading.appendChild(h3);

         var h4 = document.createElement('th');
         h4.innerHTML="Qty";
         h4.className="text-center";
         heading.appendChild(h4);

         var h5 = document.createElement('th');
         heading.appendChild(h5);

         lst.appendChild(heading);

        for(let i=0; i<cart.length; i++){

             var tr = document.createElement("TR");
             var btn_add = document.createElement("button");
             var btn_sub = document.createElement("button");
             var btn_del = document.createElement("button");
             btn_add.innerHTML = "+";
             btn_sub.innerHTML = "-";
             btn_del.innerHTML = "x";
             btn_add.className= "btn btn-custom-round";
             btn_add.setAttribute("id","add" + cart[i].item);
             btn_del.className= "btn btn-custom";
             btn_del.setAttribute("id","del" +  cart[i].item);
             btn_sub.className= "btn btn-custom"
             btn_sub.setAttribute("id","sub" + cart[i].item);
             btn_add.setAttribute("onclick","editCart()");
             btn_sub.setAttribute("onclick","editCart()");
             btn_del.setAttribute("onclick","deleteItem(this)");

             var td1 = document.createElement("TD");
             td1.setAttribute("class","text-center");
             td1.width = '50';
             td1.appendChild(btn_del);
             tr.appendChild(td1);

             var td2 = document.createElement("TD");
             td2.setAttribute("class","text-center");
             td2.id= cart[i].item;
             td2.width = '50';
             td2.appendChild(document.createTextNode(cart[i].item));
             tr.appendChild(td2);

             var td3 = document.createElement("TD");
             td3.setAttribute("class","text-center");
             td3.width = '50';
             td3.appendChild(btn_sub);
             tr.appendChild(td3);

             var td4 = document.createElement("TD");
             td4.setAttribute("class","text-center");
             td4.width = '50';
             td4.appendChild(document.createTextNode(cart[i].qty));
             tr.appendChild(td4);

             var td5 = document.createElement("TD");
             td5.setAttribute("class","text-center");
             td5.width = '50';
             td5.appendChild(btn_add);
             tr.appendChild(td5);

             lst.appendChild(tr);

            total = total + (cart[i].price * cart[i].qty);
            tHolder.innerHTML = total;
            sessionStorage.setItem('Total',total);

         }
    }
}

function editCart(){

var cart = grabCart();

    if(cart == null){
    sessionStorage.setItem('Cart', JSON.stringify([{
                                        item: '0',
                                        price: 0,
                                        qty: 0,
                                   }]));
    }

    var id = parseString(event.srcElement.id);

    for( let i =0; i < cart.length; i++){
        if(cart[i].item === id){
            if (event.srcElement.id.substr(0,3) === "add"){
                cart[i].qty +=1;
                break;
            }else{
            if(cart[i].qty==0){
                alert("You already have 0 of this item");
                break;
            }else{
                cart[i].qty -=1;
                break;
                }
            }

        }
    }

    itemNumber = 0;
    for(var j = 0; j < cart.length; j++){
        itemNumber = itemNumber + cart[j].qty;
    }

    document.getElementById('cart-number').innerHTML = itemNumber; 
    sessionStorage.setItem('Cart',JSON.stringify(cart));

    displayCart();
}

function deleteItem(item){
    let cart = grabCart();
    var row = item.parentNode.parentNode.rowIndex;
    var itemId = parseString(event.srcElement.id);
    var total = parseFloat(document.getElementById('total').innerHTML);
    var tHolder = document.getElementById('total');

    for(let i= 0; i< cart.length; i++){
        if(cart[i].item ===itemId){
        total = total - (cart[i].price*cart[i].qty);
        tHolder.innerHTML = total;
        cart.splice(i,1);
        break;
        }
    }

    itemNumber = 0;
    for(var j = 0; j < cart.length; j++){
        itemNumber = itemNumber + cart[j].qty;
    }


    document.getElementById('cart-number').innerHTML = itemNumber; 

    document.getElementById("order_table").deleteRow(row);

    sessionStorage.setItem('Cart',JSON.stringify(cart));
    sessionStorage.setItem('Total',total);
}


