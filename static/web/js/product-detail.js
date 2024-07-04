$(document).ready(function () {
  // Function to update prices and offer percent for a specific card
  function updatePricesAndOffer(card) {
    var selectedRadio = card.find('input[name="size"]:checked');
    if (selectedRadio.length > 0) {
      var salePrice = selectedRadio.data("sale-price");
      var originalPrice = selectedRadio.data("regular-price");
      var offerPercent = parseFloat(
        ((originalPrice - salePrice) / originalPrice) * 100
      ).toFixed(2);
      var savedAmount = originalPrice - salePrice;
      card.find(".current-price").text("₹" + salePrice);
      card.find(".text-content").text("₹" + originalPrice);
      card.find(".offer_percent").text(offerPercent + "% off");
      card.find(".saved-price").text("Saved Price ₹" + savedAmount);
    }
  }

  // Event listener for radio button click within each card
  $('input[name="size"]')
    .off("click")
    .on("click", function () {
      var card = $(this).closest(".cart-div");
      updatePricesAndOffer(card);
    });

  // Event listener for add cart button click
  $("#cart-add-btn").click(function () {
    var product_Id = $('input[name="size"]:checked').val();
    var quantity = $("input[name='quantity']").val();
    var url = "/cart-add/?product_id=" + product_Id + "&quantity=" + quantity;
    $.ajax({
      type: "GET",
      url: url,

      success: function (data) {
        $(".header_cart_count").html(data.cart_count);
        window.location.href = "/cart/";
      },
      error: function (data) {
        if (data.status == "401") {
          window.location.href = "/accounts/login/";
        } else {
          // Display error message with SweetAlert
          Swal.fire({
            title: "Error",
            icon: "error",
            text:
              data.responseJSON.message ||
              "An error occurred while adding the item to the cart.",
          });
        }
      },
    });
  });

  $(".wishlist-btn").click(function () {
    var product = $(this).data("product");
    var url = "/wishlist/add/?product_id=" + product;
    $.ajax({
      type: "GET",
      url: url,
      success: function (data) {
        console.log("add to whislist");

        if (data.alreadyInWishlist) {
          // Redirect to the wishlist page
          window.location.href = "/wishlist";
        }
      },
      error: function (data) {
        if (data.status == "401") {
          window.location.href = "/accounts/login/";
        } else {
          console.log(data.responseJSON.message, "alert-danger");
        }
      },
    });
  });

});
