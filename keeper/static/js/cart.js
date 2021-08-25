function addProduct(){
    const qnfield = document.getElementById('quantityfield').value;
    const nextqn = parseFloat(qnfield) + 1;

    document.getElementById('currentquantity').innerHTML = nextqn;
    document.getElementById('quantityfield').value = nextqn;

    calculateTotal();
}

function removeone(){
    const qnfield = document.getElementById('quantityfield').value;
    const prevqn = qnfield <= 1 ? 0 : parseFloat(qnfield) - 1;

    document.getElementById('currentquantity').innerHTML = prevqn;
    document.getElementById('quantityfield').value = prevqn;

    calculateTotal();
}

function removeProduct(pn){
    var product_name = pn;
    let storageProducts = JSON.parse(localStorage.getItem('products'));
    let products = storageProducts.filter(product => product.product_name !== product_name );
    localStorage.setItem('products', JSON.stringify(products));
}

function calculateTotal() {
    var total = 0;
    $("#quantityfield").each(function () {
        var quantity = $(this).val(),
          price = $(this).data("price");

        total += parseFloat(quantity * price);
      });

    console.log("Rs." + total);

}
calculateTotal();
function showcart(){
    let products =JSON.parse(localStorage.getItem('products'));
    console.log(products);
}
