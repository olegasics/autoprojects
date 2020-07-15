function clickSaveOrder(order_id) {

    var $saveBtn = $('#save-order-' + order_id)
    var $editBtn = $('#edit-order-' + order_id)
    var $cargoText = $('#cargo-text-' + order_id)
    var $cargoEdit = $('#cargo-edit-' + order_id)
    var $stateCustomOrderText = $('#order-state-text-' + order_id)
    var $stateCustomOrderEdit = $('#custom-order-status-edit-' + order_id)
    var $stateOrderTextDL = $('#order-state-dl-' + order_id)
    var $ttn = $('#ttn-' + order_id)
    var $invoice = $('#invoice-' + order_id)
    var $projectName = $('#project-name-' + order_id)
    

    $.ajax({
        
        type: "PATCH",
        url: '/orders/' + order_id,
        data:{
            'name': $projectName.val(),
            'invoice': $invoice.val(), 
            'ttn': $ttn.val(),
            'cargo': $cargoEdit.val(),
            'state_order_text_custom': $stateCustomOrderEdit.val(),
            'state_order_text_dl': $stateOrderTextDL.val()
        
        },
        
        success: function(response) {
            $invoice.prop('disabled', true)
            $projectName.prop('disabled', true)
            $ttn.prop('disabled', true)
            $cargoEdit.prop('hidden', true)
            $cargoText.prop('hidden', false)
            $cargoText.html($cargoEdit.val())
            $stateCustomOrderEdit.prop('hidden', true)
            $stateCustomOrderText.html($stateCustomOrderEdit.val())
            $stateCustomOrderText.prop('hidden', false)

            $saveBtn.prop('hidden', true)
            $editBtn.prop('hidden', false)

        },
        error: function(error) {
            console.log(error);
        }
      
    });

}

function clickEditOrder(order_id) {
    var $editBtn = $('#edit-order-' + order_id)
    var $saveBtn = $('#save-order-' + order_id)
    var $cargoText = $('#cargo-text-' + order_id)
    var $cargoEdit = $('#cargo-edit-' + order_id)
    var $stateOrderText = $('#order-state-text-' + order_id)
    var $stateOrderEdit = $('#custom-order-status-edit-' + order_id)
    var $stateOrderTextDL = $('#order-state-dl-' + order_id)
    var $projectName = $('#project-name-' + order_id)
    var $invoice = $('#invoice-' + order_id)
    var $ttn = $('#ttn-' + order_id)

    $projectName.prop('disabled', false)
    $invoice.prop('disabled', false)
    $ttn.prop('disabled', false)
    $cargoText.prop('hidden', true)
    $stateOrderText.prop('hidden', true)
    $cargoEdit.prop('hidden', false)
    $('#custom-order-status-edit-' + order_id + ':contains({$cargoText.val()})').attr("selected", "selected"); 
    $stateOrderEdit.prop('hidden', false)
    $stateOrderTextDL.prop('value', $stateOrderTextDL.val())
    $editBtn.prop('hidden', true)
    $saveBtn.prop('hidden', false)


}
function search() {

$.ajax({
    url: '/orders/' + $('#search_by_project').val(),
    datatype: 'html',
    success: function(response) {
        $('#result').html(response);
    }
});

}

function patchPayments() {
$.ajax({
    type: "GET",
    url: "/payments/update" ,
    data: {
        'name': $projectName.val(),
        'invoice': $invoice.val(), 
        'ttn': $ttn.val(),
        'cargo': $cargo.val()
    },
    
    success: function(response) {
        $projectName.prop('disabled', true)
        $invoice.prop('disabled', true)
        $ttn.prop('disabled', true)
        $cargo.prop('disabled', true)
        $saveBtn.prop('hidden', true)
        $editBtn.prop('hidden', false)

    },
    error: function(error) {
        console.log(error);
    }
});
}

function clickEditPayment(payment_id) {

    var $stateEdit = $('#custom-order-status-payment-' + payment_id)
    var $stateText = $('#payment-state-text-' + payment_id)
    var $savePaymentBtn = $('#save-payment-' + payment_id)
    var $editPaymentBtn = $('#edit-payment-' + payment_id)

    $editPaymentBtn.prop('hidden', true)
    $savePaymentBtn.prop('hidden', false)
    $stateText.prop('hidden', true)
    $stateEdit.prop('hidden', false)
    $('#custom-order-status-payment-' + payment_id + ':contains({$stateText.val()})').attr("selected", "selected");


}

function clickSavePayment(payment_id) {
    
    var $stateEdit = $('#custom-order-status-payment-' + payment_id)
    var $stateText = $('#payment-state-text-' + payment_id)
    var $savePaymentBtn = $('#save-payment-' + payment_id)
    var $editPaymentBtn = $('#edit-payment-' + payment_id)

    $.ajax({
        type: "PATCH",
        url: '/payments/',

        data: {
            'payment_id': payment_id,
            'state_payment': $stateEdit.val()
        },

        success: function(response) {
            $savePaymentBtn.prop('hidden', true)
            $editPaymentBtn.prop('hidden', false)
            $stateEdit.prop('hidden', true)
            $stateText.html($stateEdit.val())
            $stateText.prop('hidden', false)

        },

        error: function(response) {
            console.log(response)
        }

    });

}

function clickApprove(payment_id) {

    var $stateText = $('#payment-state-text-' + payment_id)
    var $approve = $('#approve-' + payment_id)
    var $sendPayment = $('#send-in-payment-' + payment_id)

    $.ajax({
        type: 'GET',
        url: '/payments/approve/' + payment_id,
        success: function(response) {
            $sendPayment.prop('hidden', true)
            $approve.prop('hidden', false)
            $stateText.html('Ожидает оплаты')

        },

        error: function(response) {
            console.log(response)
        }

    });
}

function clickPaid(payment_id) {
    var $paidBtn = $('#paid-invoice-' + payment_id)
    var $uploadPPForm = $('#upload-pp-form-' + payment_id)
    var $stateText = $('#payment-state-text-' + payment_id)

    $paidBtn.prop('hidden', true)
    $stateText.html('Оплачено')
    $uploadPPForm.prop('hidden', false)

}



