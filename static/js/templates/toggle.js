$('.not_hidden_order_info').click(function(){
    var hid = $(this).next('tr');

    if(hid.is(":hidden")) {
        hid.show();
    }
    else {
        hid.hide();
    }
});


// $('.not_hidden_order_info').click(function(){

//     $(this).next('tr').toggle();
// })