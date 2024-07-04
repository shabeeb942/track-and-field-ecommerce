 /**=====================
     Quantity 2 js
==========================**/
$(".addcart-button").click(function () {
    var productId = $(this).data('product-id');
    $("#quantity-" + productId).val('1');
    $(this).closest('.var-modal').find('.qty-box').addClass("open");
});

 $('.add-to-cart-box').on('click', function () {
     var $qty = $(this).siblings(".qty-input");
     var currentVal = parseInt($qty.val());
     if (!isNaN(currentVal)) {
         $qty.val(currentVal + 1);
     }
 });

 $('.qty-left-minus').on('click', function () {
     var $qty = $(this).siblings(".qty-input");
     var _val = $($qty).val();
     if (_val == '1') {
         var _removeCls = $(this).parents('.cart_qty');
         $(_removeCls).removeClass("open");
     }
     var currentVal = parseInt($qty.val());
     if (!isNaN(currentVal) && currentVal > 0) {
         $qty.val(currentVal - 1);
     }
 });

 $('.qty-right-plus').click(function () {
     if ($(this).prev().val() < 1000) {
         $(this).prev().val(+$(this).prev().val() + 1);
     }
 });
 
 $(document).ready(function () {
    $('.addcart-button').each(function() {
        var qty = $(this).data('quantity');
        if (qty > 0) {
            $(this).closest('.var-modal').find('.qty-box').addClass("open");
        }
    });
});


