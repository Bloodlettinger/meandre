var get_customer_code = function(action) {
    var $ = django.jQuery;
    $.ajax({
        type: "GET",
        url: "/admin/storage/get_customer_code/",
        data: {action: action},
        complete: function(res, status) {
            $("#id_code").val(res.responseText);
            console.log(status);
        }
    });
};
