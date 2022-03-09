
var shoppingCart = (function() {
  cart = [];

  function Item(name, price, count, proid, shopname,proimage) {
    this.name = name;
    this.price = price;
    this.count = count;
    this.proid = proid;
    this.shopname = shopname;
    this.proimage = proimage;
  }

  // Save cart
  function saveCart() {
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
  }

    // Load cart
  function loadCart() {
    cart = JSON.parse(localStorage.getItem('shoppingCart'));
  }
  if (localStorage.getItem("shoppingCart") != null) {
    loadCart();
  }


  var obj = {};

  // Add to cart
  obj.addItemToCart = function(name, price, count, proid, shopname,proimage) {
    for(var item in cart) {
      if(cart[item].name === name) {
        cart[item].count ++;
        saveCart();
        return;
      }
    }
    var item = new Item(name, price, count,proid, shopname, proimage);
    cart.push(item);
    saveCart();
  }
  // Set count from item
  obj.setCountForItem = function(name, count) {
    for(var i in cart) {
      if (cart[i].name === name) {
        cart[i].count = count;
        break;
      }
    }
  };
  // Remove item from cart
  obj.removeItemFromCart = function(name) {
      for(var item in cart) {
        if(cart[item].name === name) {
          cart[item].count --;
          if(cart[item].count === 0) {
            cart.splice(item, 1);
          }
          break;
        }
    }
    saveCart();
  }

  // Remove all items from cart
  obj.removeItemFromCartAll = function(name) {
    for(var item in cart) {
      if(cart[item].name === name) {
        cart.splice(item, 1);
        break;
      }
    }
    saveCart();
  }

  // Clear cart
  obj.clearCart = function() {
    cart = [];
    saveCart();
  }

  // Count cart
  obj.totalCount = function() {
    var totalCount = 0;
    for(var item in cart) {
      totalCount += cart[item].count;
    }
    return totalCount;
  }

  // Total cart
  obj.totalCart = function() {
    var totalCart = 0;
    for(var item in cart) {
      totalCart += cart[item].price * cart[item].count;
    }
    return Number(totalCart.toFixed(2));
  }

  // List cart
  obj.listCart = function() {
    var cartCopy = [];
    for(i in cart) {
      item = cart[i];
      itemCopy = {};
      for(p in item) {
        itemCopy[p] = item[p];

      }
      itemCopy.total = Number(item.price * item.count).toFixed(2);
      cartCopy.push(itemCopy)
    }
    return cartCopy;
  }


  return obj;
})();


// Add item
$('.add-button').click(function(event) {
  event.preventDefault();
  var name = $(this).data('name');
  var price = Number($(this).data('price'));
  var proid = Number($(this).data('proid'));
  var shopname = $(this).data('shopname');
  var proimage = $(this).data('proimage');
  shoppingCart.addItemToCart(name, price, 1, proid, shopname, proimage);
  displayCart();
});

// Clear items
$('.clear-cart').click(function() {
  shoppingCart.clearCart();
  displayCart();
});


function displayCart() {
  var cartArray = shoppingCart.listCart();
  var totalCart = shoppingCart.totalCart();
  var output = "";
  var confirmout = "";

    for (var i in cartArray) {
      output += '<div class="cart-container">' +
          '                <div class="inner-cart">' +
          '					<div class="in-c">' +
          '						<img class="cart-product-img" src="'+ cartArray[i].proimage +  '" alt="product">' +
          '						<div class="cart-product-info">' +
          '							<span>' + cartArray[i].name + '</span>' +
          '							<p>' + cartArray[i].shopname + '</p>' +
          '						</div>' +
          '					</div>' +
          '					<div class="product-count">' +
          '						<button type="button" class="minus-item" data-name="' + cartArray[i].name + '">-</button>' +
          '						<input readonly="readonly" id="count" type="number" data-name="' + cartArray[i].name + '" value="' + cartArray[i].count + '">' +
          '						<button type="button" class="plus-item" data-name="' + cartArray[i].name + '">+</button>' +
          '					</div>' +
          '					<div class="price-remove">' +
          '						<p class="cart-price">' + cartArray[i].total + '</p>' +
          '						<p class="cart-remove" data-name="' + cartArray[i].name + '">Remove</p>' +
          '					</div>' +
          '                </div>' +
          '            </div>';
      confirmout += '<div class="cart-container">' +
          '                <div class="inner-cart">' +
          '					<div class="in-c">' +
          '						<img class="cart-product-img" src="'+ cartArray[i].proimage +  '" alt="product">' +
          '						<div class="cart-product-info">' +
          '							<span>' + cartArray[i].name + '</span>' +
          '							<p>' + cartArray[i].shopname + '</p>' +
          '						</div>' +
          '					</div>' +
          '<div id="count" data-name="' + cartArray[i].name + '">Item : ' + cartArray[i].count + '</div>'+
          '					<div class="price-remove">' +
          '						<p class="cart-price">₹' + cartArray[i].total + '</p>' +
          '					</div>' +
          '                </div>' +
          '            </div>';
    }
    var billoutput = '<div class="bill-container">' +
        '					<h3 class="bill-heading">Bill Details</h3>' +
        '					<div class="bill-brief-con">' +
        '						<div class="bill-brief">' +
        '							<p class="item-font">Item Total</p>' +
        '							<p class="item-price">₹' + totalCart + '</p>' +
        '						</div>' +
        '						<div class="total-border"></div>' +
        '						<div class="bill-brief">' +
        '							<p class="item-font-bold">Total(inc. GST)</p>' +
        '							<p class="item-font-bold b">₹' + totalCart + '</p>' +
        '						</div>' +
        '					</div>' +
        '					<div class="search-catagory">' +
        '						<select name="order_type" id="order_type" onchange="changeOrderType();">' +
        '							<option value="HOME_DELIVERY" selected>HOME DELIVERY</option>' +
        '							<option value="PICK_UP">SELF PICKUP</option>' +
        '						</select>' +
        '					</div>' +
        '					<div id="datetime" class="datetime">' +
        '						<input type="datetime-local" id="pick_up_date" name="pick_up_date">' +
        '					</div>' +
        '<!--					<div class="coupencode-con">-->' +
        '<!--						<input type="text" />-->' +
        '<!--						<button class="coupencode-button">Apply</button>-->' +
        '<!--					</div>-->' +
        '					<button type="submit" class="checkout-button">Checkout' +
        '						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right-circle" viewBox="0 0 16 16">' +
        '						  <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8zm15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>' +
        '						</svg>' +
        '					</button>' +
        '				</div>' +
        '<input type="hidden" name="product_list" id="product_list" />' +
        '            <input type="hidden" name="total" id="total" />';

    var confirmbill = '<div class="bill-container">' +
        '						<div class="bill-brief">' +
        '							<p class="item-font-bold">Total(inc. GST)</p>' +
        '							<p class="item-font-bold b">₹' + totalCart + '</p>' +
        '						</div>' +
        '					</div>' +
        '					<div class="search-catagory">' +
        '						<select name="order_type" id="order_type" onchange="changeOrderType()">' +
        '							<option value="HOME_DELIVERY" selected>HOME DELIVERY</option>' +
        '							<option value="PICK_UP">SELF PICKUP</option>' +
        '						</select>' +
        '					</div>' +
        '					<div id="datetime" class="datetime">' +
        '						<input type="datetime-local" id="pick_up_date" name="pick_up_date">' +
        '					</div>' +
        '<!--					<div class="coupencode-con">-->' +
        '<!--						<input type="text" />-->' +
        '<!--						<button class="coupencode-button">Apply</button>-->' +
        '<!--					</div>-->' +
        '					<button type="submit" class="checkout-button">Checkout' +
        '						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right-circle" viewBox="0 0 16 16">' +
        '						  <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8zm15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>' +
        '						</svg>' +
        '					</button>' +
        '				</div>' +
        '<input type="hidden" name="product_list" id="product_list" />' +
        '            <input type="hidden" name="total" id="total" />';

    $('#showcart').html(output);
    $('#confirmcart').html(confirmout);
    $('#billcart').html(billoutput);
    $('.total-cart').html(shoppingCart.totalCart());
    $('.total-count').html(shoppingCart.totalCount());

    document.getElementById('product_list').value = JSON.stringify(shoppingCart.listCart());
    document.getElementById('total').value = shoppingCart.totalCart().toString()

}
// Delete item button

$('#showcart').on("click", ".cart-remove", function(event) {
  var name = $(this).data('name')
  shoppingCart.removeItemFromCartAll(name);
  displayCart();
})


// -1
$('#showcart').on("click", ".minus-item", function(event) {
  var name = $(this).data('name')
  shoppingCart.removeItemFromCart(name);
  displayCart();
})
// +1
$('#showcart').on("click", ".plus-item", function(event) {
  var name = $(this).data('name')
  shoppingCart.addItemToCart(name);
  displayCart();
})

// Item count input
$('#showcart').on("change", "#count", function(event) {
   var name = $(this).data('name');
   var count = Number($(this).val());
  shoppingCart.setCountForItem(name, count);
  displayCart();
});

displayCart();