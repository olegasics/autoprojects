
function clickCreateCustomOrder() {

    $.ajax({
        type: "POST",
        url: "/orders/",
        data: {
            'name': $('#custom_order_project').val(),
            'invoice': $('#custom_order_invoice').val(),
            'cargo': $('#custom_order_cargo').val(),
            'status': $('#custom_order_status').val(),
            'sender': $('#custom_order_sender').val(),
            'receiver': $('#custom_order_receiver').val(),
            'document': $('#custom_order_document').val(),
            'carrier': $('#custom_order_carrier').val(),
            'ttn': $('#custom_order_ttn').val(),
            'send_city': $('#custom_order_send_city').val(),
            'delivery_city': $('#custom_order_delivery_city').val(),
            'send_date': $('#custom_order_send_date').val(),
            'delivery_date': $('#custom_order_delivery_date').val(),
            'weight': $('#custom_order_weight').val(),
            'volume': $('#custom_order_volume').val(),
            'sum': $('#custom_order_sum').val()
        },
        
        success: function(response) {
            window.location.reload()
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}



function clickCreateManager() {

    $.ajax({
        type: "POST",
        url: "/managers/create",
        data: {
            'name': $('#manager-name').val(),
            'small_name': $('#manager-small-name').val(),
            'number_phone': $('#manager-number-phone').val()
        },
        
        success: function(response) {
            window.location.reload()
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function clickCreateProject() {

    $.ajax({
        type: "POST",
        url: "/projects/create",
        data: {
            'name': $('#project-name').val(),
            'manager_small_name': $('#manager-small-name').val(),
            'customer': $('#customer').val()
        },
        
        success: function(response) {
            window.location.reload()
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function sendInPayment(order_id) {
    var $sendPayment = $('#send-payment-order-' + order_id);
    var $uploadInvoiceCargoForm = $('#upload-invoice-form-' + order_id)
    var $uploadInvoiceCargoBtn = $('#upload-invoice-' + order_id)

    $.ajax({
        type: "POST",
        url: "/payments/",
        data: {
            'order_id': order_id
        },
        
        success: function(response) {
            $sendPayment.html('Отправлено')
            $uploadInvoiceCargoForm.prop('hidden', false)
            $uploadInvoiceCargoBtn.html('Отправлено')
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function createProvider(project_id) {

    var $name = $('#name-provider');
    var $createProviderBtn = $('#create-provider');
    $.ajax({
        type: "POST",
        url: "/providers/",
        data: {
            'name': $name.val(),
            'project_id': project_id
        },

        success: function(response) {
            $createProviderBtn.html('Создан')
            console.log('success')

        },
        error: function(error) {
            console.log(error);
        }
    });
}




