$.fn.extend({
    scrollTo: function(obj, speed, easing) {
        return this.each(function() {
            var targetOffset = obj.offset().top;
            $(this).animate({scrollTop: targetOffset}, speed, easing);
        });
    },
    centrify: function() {
        return $(this).css({
            'top':($(window).height()/2 - $(this).height()/2)+'px',
            'left':($(window).width()/2 - $(this).width()/2)+'px'
        });
    },
    alignCenter: function() {
        var marginLeft = - $(this).width()/2 + 'px';
        var marginTop = - $(this).height()/2 + 'px';
        var widthPopup = $(this).width()/2 + 'px';
        return $(this).css({'margin-left':marginLeft, 'margin-top':marginTop, 'width':widthPopup});
    },
    togglePopup: function() {
        var popup = $('#popup'),
            opaco = $('#opaco'),
            event_name = (window.chrome && $.browser.webkit) ? 'keydown' : 'keypress';
        if (popup.hasClass('hide')) {
            opaco.height($(document).height()).toggleClass('hide').fadeTo('slow', 0.7);
            popup.html($(this).html()).alignCenter().toggleClass('hide');
            $(document).bind(event_name,
                             function(e) {
                                 var code = (e.keyCode ? e.keyCode : e.which);
                                 if (code == 27) {
                                     popup.togglePopup();
                                 }
                             });
        } else {
            $(document).unbind(event_name);
            opaco.fadeTo('slow', 0.0,
                         function() {
                             popup.toggleClass('hide');
                             $(this).toggleClass('hide');
                         });
        }
    },
    animateHighlight: function(highlightColor, duration) {
        var highlightBg = highlightColor || "#FFFF9C";
        var animateMs = duration || 1500;
        var originalBg = this.css("backgroundColor");
        this.stop().css("background-color", highlightBg).animate({backgroundColor: originalBg}, animateMs);
    }
});

var setCropData = function (o, pk) {
    var area = $('.fancybox-title');
    $('#id_is_cropped', area).val('on');
    $('#id_point_x', area).val(o.x);
    $('#id_point_y', area).val(o.y);
    $('#id_width', area).val(o.w);
    $('#id_height', area).val(o.h);
    $('#id_image', area).val(pk);
}

var updateElementIndex = function(el, prefix, ndx) {
    var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
    var replacement = prefix + "-" + ndx;
    if ($(el).attr("for")) {
        $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    }
    if (el.id) {
        el.id = el.id.replace(id_regex, replacement);
    }
    if (el.name) {
        el.name = el.name.replace(id_regex, replacement);
    }
};

var updateManagementData = function(prefix) {
    var area = $('fieldset.module');
    var container = $('#image_list');
    var total = $('input[name$=position]', container).length;
    $('input[name='+prefix+'-TOTAL_FORMS]', area).val(total);
    $('input[name='+prefix+'-INITIAL_FORMS]', area).val(total);
}

var openCropBox = function() {
    var frame = $(this).parent(),
        obj_pk = $(this).data('id'),
        image_url = $(this).data('url');
    $.fancybox.open(
        [{href: image_url}],
        {
            padding: 2,
            beforeShow: function() {
                this.title = $('#done_form_container').html();
            },
            afterShow: function() {
                var area = $('.fancybox-title'),
                    image = $('.fancybox-image');

                $('#id_image', area).val(obj_pk);
                $('#id_shown_width', area).val(image.width());
                $('#id_shown_height', area).val(image.height());

                image.Jcrop({
                    onSelect: function(o) { return setCropData(o, obj_pk); },
                    onChange: function(o) { return setCropData(o, obj_pk); }
                });

                $('form', area).each(function() {
                    $(this).ajaxForm({
                        dataType: 'text',
                        beforeSubmit: function() {
                            // $('input[name=inline_index]', area).val();
                            $('input[name=submit]', area).attr('disabled', 'disabled');
                        },
                        success: function(data, status, xhr) {
                            $('input[name=submit]', area).removeAttr('disabled');
                            $.fancybox.close();

                            switch(xhr.status) {
                                case 200: // changed
                                    $('img', frame).replaceWith($('img', data));
                                    $('div.header', frame).replaceWith($('div.header', data));
                                    $('div.footer', frame).replaceWith($('div.footer', data));
                                    $('#image_list .frame img').click(openCropBox);
                                    $.jGrowl('Saved!');
                                    break;
                                case 204: // removed
                                    frame.remove();
                                    $.jGrowl('Deleted!');

                                    // refresh formset input indexes
                                    $('#image_list .frame').each(function(index, frame) {
                                        $(frame).find('input').each(function() {
                                            updateElementIndex(this, 'images_set', index);
                                        });
                                    });
                                    updateManagementData('images_set');
                                    break;
                                default:
                                    $.jGrowl('Response status: ' + xhr.status);
                            }
                        },
                        error: function(xhr, status, errMsg) {
                            $.jGrowl('Error: ' + errMsg);
                        }
                    })
                });
            },
            helpers: {
                title: { type: 'outside'}
            }
        });
}
