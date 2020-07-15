window.onload = function() {
    var orderEnd = document.querySelector('#shest0');

    orderEnd.onclick = function() {
        if (orderEnd.checked) {

            window.location.replace('/orders/?ended=1')
            
        } else {
            window.location.replace('/orders/?ended=0')
        }
    }



}


