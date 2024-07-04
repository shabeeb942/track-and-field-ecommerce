
$(document).ready(function () {
    var cart_total = $("#cart_total").text();
    var cart_total = cart_total.replace('₹', '');
    var shipping_price = $("#shipping_price").data('shipping_price');
    var sub_total = parseFloat(cart_total) + parseFloat(shipping_price);
    $("#cart_total").text("₹"+sub_total.toFixed(2));
    $("#total_price").val(sub_total.toFixed(2));
    // minus to cart`
    $(".cart-minus-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var url = "/cart-minus/?item_id=" + product_Id;
        var qty_value = $("#quantity-" + product_Id);
        var total_amt = $("#total-" + product_Id);
        var total_mob = $("#total-mobile-" + product_Id);

        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
            //   if (data.quantity == '1') {window.location.reload()}
              qty_value.val(data.quantity);
              total_amt.text("₹"+data.total_price);
              $('#cart_total').html("₹"+data.cart_total);
              sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
              $("#sub_total").text("₹"+sub_total.toFixed(2));
              total_mob.text("₹"+data.total_price);

              
                
            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });
    // Add to cart
    // $(".cart-add-btn").click(function () {
    //     var product_Id = $(this).data("product_id");
    //     var url = "/cart-add/?product_id="+product_Id; 
    //     var qty_value = $("#quantity-" + product_Id);
    //     var total_amt = $("#total-" + product_Id);
    //     var total_mob = $("#total-mobile-" + product_Id);
    //     $.ajax({
    //         type: "GET",
    //         url: url,
            
    //         success: function (data) {
    //           qty_value.val(data.quantity);
    //           total_amt.text("₹"+data.total_price);
    //           total_mob.text("₹"+data.total_price);
    //           $('#cart_total').html("₹"+data.cart_total);
    //           sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
    //           $("#sub_total").text("₹"+sub_total.toFixed(2));
              
                
    //         },
    //         error: function (data) {
    //             // Display error message
    //             console.log("error")
    //         }
    //     });
    // });
   
    $(".close_button").click(function () {
        var product_Id = $(this).data("product_id");
        var url = "/cart-item-clear/"+product_Id; 

        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
                total = parseFloat(data.cart_total) + parseFloat(shipping)
                $('#cart_total').html("₹"+total.toFixed(2));
                $('.badge').html(data.cart_count)
                if (data.cart_count == 0) {
                    window.location.reload();
                }

            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });
    $('.cart-qty-number').addClass('form-control');
    $('.update-qty-btn').click(function () {
        card = $(this).closest('.qty-div');
        var qty = card.find('input[name="item_qty"]').val();
        
        var product_Id = $(this).data("product_id");
        var url = "/cart-update/?product_id="+product_Id+"&quantity="+qty; 
        var total_amt = $("#total-" + product_Id);
        var total_mob = $("#total-mobile-" + product_Id);

        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
                
              total_amt.text("₹"+data.total_price);
              total_mob.text("₹"+data.total_price);
              $('#cart_total').html("₹"+data.cart_total);
              sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
              $("#sub_total").text("₹"+sub_total.toFixed(2));
            },
            error: function (data) {
                // Display error message
                console.log("error")
            }
        });
    });

    $('.cart-qty-number').on('input', function() {
        var quantity = $(this).val(); // Get the entered quantity
        var productId = $(this).data('product_id'); // Get the product ID
        var card = $(this).closest('.product-detail');
        var user_price = card.find('.user_price')
        var shipping = $('#shipping_price').data('shipping_price');
        console.log(shipping)
        // Make an AJAX request to fetch the price based on quantity
        $.ajax({
            url: '/get_price/',  // URL to your view that handles the AJAX request
            type: 'GET',
            data: {
                'product_id': productId,
                'quantity': quantity
            },
            success: function(data) {
                // console.log("success============",data.price);
                user_price.text(data.price);
                $('#product-price').text('Product Price: ' + data.price); // Update the displayed price
               
                var url = "/cart-update/?product_id="+productId+'&quantity='+quantity+"&price="+data.price; 
                var qty_value = $("#quantity-" + productId);
                var total_amt = $("#total-" + productId);
                var total_mob = $("#total-mobile-" + productId);
                $.ajax({
                    type: "GET",
                    url: url,
                    
                    success: function (data) {
                    // console.log("222222222============",data);
                    qty_value.val(data.quantity);
                    total_amt.text("₹"+data.total_price);
                    total_mob.text("₹"+data.total_price);
                    total = parseFloat(data.cart_total) + parseFloat(shipping)
                    $('#cart_total').html("₹"+total.toFixed(2));
                    // sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
                    // $("#sub_total").text("₹"+sub_total.toFixed(2));
                    
                        
                    },
                    error: function (data) {
                        // Display error message
                        console.log("error")
                    }
                });
                    },
                    error: function(xhr, status, error) {
                        console.error(xhr.responseText); // Log any errors to console
                    }
                });
    });   

    
  });