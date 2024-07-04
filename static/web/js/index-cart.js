
$(document).ready(function () {
    
    // minus to cart`
    $(".qty-minus").click(function () {
        var product_id = $(this).data("product-id");
        var url = "/cart-minus/?item_id=" + product_id;
        var qty = $("#quantity-" + product_id).val();
    
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                // If the quantity becomes less than 1, remove the item from the cart
                if (qty < 1) {
                    $.ajax({
                        type: "GET",
                        url: "/cart-item-clear/" + product_id,
                        success: function (data) {
                            
                        
                        },
                        error: function (data) {
                            console.log("Error removing item");
                        }
                    });
                }
            },
            error: function (data) {
                console.log("Error decrementing quantity");
            }
        });
    });

    // Add to cart
    $(".qty-plus").click(function () {
        var product_Id = $(this).data("product-id");
        var url = "/cart-add/?product_id="+product_Id; 

        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {

                $('.badge').html(data.cart_count)

            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });

    $(".qty-plus-btn").click(function () {
        var product_Id = $(this).data("product-id");
        var url = "/cart-add/?product_id="+product_Id; 

        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
              
                console.log(data)
                console.log("sussess")
                $('.badge').html(data.cart_count)
                if (data.quantity <= 0) {window.location.url = "/"} 

                
            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });

    $(".close_button").click(function () {
        var product_Id = $(this).data("product_id");
        var url = "/cart-item-clear/"+product_Id; 

        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
              console.log("sussecss")
              
                
            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });



    
  });