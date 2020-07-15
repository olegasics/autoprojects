window.onload = function() {
    var logistOrderEnd = $('#shest1');

    logistOrderEnd.onclick = function() {
        if (logistOrderEnd.checked) {

            window.location.replace('/logistics/?ended=1')

        } else {
            window.location.replace('/logisctics/?ended=0')
        }
    }



}
