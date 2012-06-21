$(document).ready(function() {
    var timer = null;

    function reset_counter(event, lang) {
        var value = event.target.value;
        if (timer) {
            clearTimeout(timer);
        }
        timer = setTimeout(function() {
            $('#teaser_preview_'+lang).html(value);
        }, 2000);
    }

    function init_listener(lang) {
        $('#teaser_preview_'+lang).html($('#id_desc_short_'+lang).html());
        $('#id_desc_short_'+lang).keyup(function(event) {
            reset_counter(event, lang);
        });
    }

    init_listener('ru');
    init_listener('en');
});
