
$(document).ready(function() {

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    var total_price=0;
    var products_command=[];
    var calc_cumul = undefined;

    function displayCategories(categories){
        $("#categories").html("");
        var cat_buttons = "";
        for (var i=0; i<categories.length; i++){
            for(var key in categories[i])
                $("#categories").append('<button type="button" class="btn btn-default btn-info category btn-category" id="'+key+'">'+categories[i][key]+'</button>\n');
        }
    }

    function displayAriane(categories){
        $("#ariane").html("");
        var cat_buttons = "";
        for (var i=categories.length-1; i>=0; i--){
            for(var key in categories[i])
                $("#ariane").append('<button type="button" class="btn btn-default btn-warning category" id="'+key+'">'+categories[i][key]+'</button><div class="glyphicon glyphicon-chevron-right"></div>\n');
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

    function displayCommandProducts(){
        var happy_hour = $("#happy_hour").val();
        $("#command").html("");
        total_price = 0;
        for (var i=0; i<products_command.length; i++){
            var product_info = products_command[i];
            if (happy_hour=="True"){
                product_info.price = product_info.happy_hour
            }
            total_price += product_info.price;
            $("#command").append("<li data-product='"+i+"' class='drag-element col-sm-12 col-md-12 col-lg-12'>" +
                                 "<span class='col-sm-1 col-md-1 col-lg-1 glyphicon glyphicon-remove delete' id="+i+"></span>"+
                                 "<div class='col-sm-9 col-md-9 col-lg-9'><b>"+product_info.name+" :</b> "+product_info.price+"€</div>" +
                                 "<button type='button' class='col-sm-2 col-md-2 col-lg-2 btn btn-default btn-product glyphicon glyphicon-gift free' id="+i+"></button>" +
                                 "<button type='button' class='col-sm-2 col-md-2 col-lg-2 btn btn-default btn-product glyphicon glyphicon-header gift' id="+i+"></button>" +
                                 "</li>");
        }
        $("#total_price").html(total_price);
    }

    function addProduct(product_info){
        var multiply = 1;
        if (calc_cumul != undefined){
            multiply = parseInt(calc_cumul);
        }
        for (var mult=0; mult<multiply; mult++){
            products_command.push(product_info);
        }
        calc_cumul = undefined;
        $("#calc-result").html('');
        displayCommandProducts();
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
                addProduct(product_info);
            }
        });
    });

    $('body').on("click", ".free", function(){
        var product_key = $(this).attr('id');
        products_command[product_key].price = 0;
        displayCommandProducts();
    });

    $('body').on("click", ".gift", function(){
        var product_key = $(this).attr('id');
        products_command[product_key].price = products_command[product_key].happy_hour;
        displayCommandProducts();
    });

    $('body').on("click", ".calc", function(){
        var calc_key = $(this).attr('id');
        if (calc_cumul == undefined){
            calc_cumul = "";
        }
        calc_cumul += calc_key;
        $("#calc-result").html(calc_cumul);
    });
    //calc-del
    $('body').on("click", "#calc-del", function(){
        calc_cumul = undefined;
        $("#calc-result").html('');
    });

    $('body').on("click", ".delete", function(){
        var product_key = $(this).attr('id');
        products_command.splice(product_key,1);
        displayCommandProducts();
    });

    $('body').on("click", "#validate", function(){
        var barman_id = $("#barman").val();
        var data_post = {
            "barman":barman_id,
            "total_price":total_price,
            "product_list":JSON.stringify(products_command)
        };
        $.ajax({
            type: 'POST',
            url: "/add_command/",
            data:data_post,
            dataType: "json",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
                if (data.data){
                    window.location.replace("/");
                }
            }
        });
    });


    $('#solde').on('show.bs.modal', function (e) {
        $.ajax({
            type: 'GET',
            url: "/get_solde/",
            success: function(data){
                $('#total-solde').html(data.total);
                $('#nb-command').html(data.nb_command);
            }
        });
    });

    $('body').on("click", ".delete-note", function(){
        var note_key = $(this).attr('id');
        var data_post = {"note_id": note_key};

        $.ajax({
            type: 'POST',
            url: "/del_note/",
            data:data_post,
            dataType: "json",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data){
               if (data.data){
                    window.location.replace("/");
                }
            }
        });
    });

});