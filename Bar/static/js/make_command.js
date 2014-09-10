$(document).ready(function() {

    var total_price=0;

    function displayCategories(categories){
        $("#categories").html("");
        var cat_buttons = "";
        for (var i=0; i<categories.length; i++){
            for(var key in categories[i])
                $("#categories").append('<button type="button" class="btn btn-default category" id="'+key+'">'+categories[i][key]+'</button>\n');
        }
    }

    function displayAriane(categories){
        $("#ariane").html("");
        var cat_buttons = "";
        for (var i=categories.length-1; i>=0; i--){
            for(var key in categories[i])
                $("#ariane").append('<button type="button" class="btn btn-default category" id="'+key+'">'+categories[i][key]+'</button>\n');
        }
    }

    function displayProducts(products){
        $("#products").html("");
        var cat_buttons = "";
        for (var i=0; i<products.length; i++){
            for(var key in products[i])
                $("#products").append('<button type="button" class="btn btn-default product" id="'+key+'">'+products[i][key]+'</button>\n');
        }
    }

    function addProduct(product_info){
        total_price += product_info.price;
        $("#total_price").html(total_price);
    }

    $('body').on("click", ".category", function(){
        var category_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: "/category_onclick/"+category_id+"/",
            success: function(data){
                var category_info = jQuery.parseJSON(data);
                displayCategories(category_info.categories);
                displayAriane(category_info.path);
                displayProducts(category_info.products);
            }
        });
    });

    $('body').on("click", ".product", function(){
        var product_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: "/product_onclick/"+product_id+"/",
            success: function(data){
                var product_info = jQuery.parseJSON(data);
                console.log(product_info);
                addProduct(product_info);
            }
        });
    });
});