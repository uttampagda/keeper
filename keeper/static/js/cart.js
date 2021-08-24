function addProduct(){
    let products = [];
    var product_name = document.getElementById("product_name").value;
    var price = document.getElementById("price").value;
    if(localStorage.getItem('products')){
        products = JSON.parse(localStorage.getItem('products'));
    }
    products.push({'product_name' : product_name + 1, 'price' : price});
    localStorage.setItem('products', JSON.stringify(products));
}

function removeProduct(){

    // Your logic for your app.

    // strore products in local storage
    var product_name = document.getElementById("product_name").value;
    var price = document.getElementById("price").value;
    let storageProducts = JSON.parse(localStorage.getItem('products'));
    storageProducts.splice(1);
    localStorage.setItem('products', JSON.stringify(storageProducts));
}
