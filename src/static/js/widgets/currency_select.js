var $ = django.jQuery || jQuery;

$(document).ready(function() {
    var currency = $('select[name="currency"]'),
        rate = $('input[name="exchange_rate"]');
    var currency_initial = currency.val(),
        rate_initial = rate.val();

    currency.change(function() {
        if (currency.val() == 1) {
            rate.val('1.0');
        } else {
            if (currency.val() == currency_initial) {
                rate.val(rate_initial);
            } else {
                rate.val('');
            }
        }
    });
});
