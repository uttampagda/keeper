function addProduct(){
    let products = [];
    var product_name = function(value,object) {object.innerHTML= value;};
    var price = function(value,object) {object.innerHTML= value;};
    if(localStorage.getItem('products')){
        products = JSON.parse(localStorage.getItem('products'));
    }
    products.push({'product_name' : product_name + 1, 'price' : price});
    localStorage.setItem('products', JSON.stringify(products));
}
