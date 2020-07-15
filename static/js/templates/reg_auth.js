function clickReg() {

    $.ajax({
        type: "POST",
        url: "/users/",
        data: {
            'email': $('#email').val(),
            'password': $('#password').val(),
            'password2': $('#password2').val(),
            'first_name': $('#first_name').val(),
            'last_name': $('#last_name').val(),
            'position': $('#position').val()
        },

        success: function(response) {
            window.location.replace('/auth');
            console.log('success')

        },
        error: function(error) {
            console.log(error);
        }
    });
}
