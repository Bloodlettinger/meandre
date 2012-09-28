django.jQuery(document).ready(function() {
    // Set this to the name of the column holding the position
    pos_field = 'position';

    // Determine the column number of the position field
    pos_col = null;

    cols = django.jQuery('#result_list tbody tr:first').children()

    for (i = 0; i < cols.length; i++) {
        inputs = django.jQuery(cols[i]).find('input[name*=' + pos_field + ']')

        if (inputs.length > 0) {
            // Found!
            pos_col = i;
            break;
        }
    }

    if (pos_col == null) {
        return;
    }

    // Some visual enhancements
    header = django.jQuery('#result_list thead tr').children()[pos_col]
    django.jQuery(header).hide();
    django.jQuery(header).children('a').text('#');

    titles = django.jQuery('#result_list tbody tr th');
    titles.append('<span class="ui-icon ui-icon ui-icon-arrowthick-2-n-s" style="float:left;"></span>');

    // Hide position field
    django.jQuery('#result_list tbody tr').each(function(index) {
        django.jQuery('td:last', this).hide();
    });

    // Determine sorted column and order
    sorted = django.jQuery('#result_list thead th.sorted');
    sorted_col = django.jQuery('#result_list thead th').index(sorted);
    sort_order = sorted.hasClass('descending') ? 'desc' : 'asc';

    if (sorted_col != pos_col) {
        // Sorted column is not position column, bail out
        console.info("Sorted column is not %s, bailing out", pos_field);
        return;
    }

    django.jQuery('#result_list tbody tr').css('cursor', 'move');

    // Make tbody > tr sortable
    django.jQuery('#result_list tbody').sortable({
        axis: 'y',
        items: 'tr',
        cursor: 'move',
        update: function(event, ui) {
            item = ui.item;
            items = django.jQuery(this).find('tr').get();

            if (sort_order == 'desc') {
                // Reverse order
                items.reverse();
            }

            django.jQuery(items).each(function(index) {
                pos_td = django.jQuery(this).children()[pos_col];
                input = django.jQuery(pos_td).children('input').first();
                label = django.jQuery(pos_td).children('strong').first();

                input.attr('value', index);
                label.text(index);
            });

            // Update row classes
            django.jQuery(this).find('tr').removeClass('row1').removeClass('row2');
            django.jQuery(this).find('tr:even').addClass('row1');
            django.jQuery(this).find('tr:odd').addClass('row2');
        }
    });
});
