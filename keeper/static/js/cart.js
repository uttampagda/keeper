function addProduct(pn,pp){
    let products = [];
    var product_name = pn;
    var price = pp;
    if(localStorage.getItem('products')){
        products = JSON.parse(localStorage.getItem('products'));
    }
    products.push({'product_name' : product_name , 'price' : price});
    localStorage.setItem('products', JSON.stringify(products));

}

function removeProduct(pn){
    var product_name = pn;
    let storageProducts = JSON.parse(localStorage.getItem('products'));



    localStorage.setItem('products', JSON.stringify(storageProducts));
}
