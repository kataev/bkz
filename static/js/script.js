/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
$(function () {
    var $win = $(window)
        , $nav = $('.subnav')
        , navTop = $('.subnav').length && $('.subnav').offset().top - 40
        , isFixed = 0

    processScroll()

    $win.on('scroll', processScroll)

    function processScroll() {
        var i, scrollTop = $win.scrollTop()
        if (scrollTop >= navTop && !isFixed) {
            isFixed = 1
            $nav.addClass('subnav-fixed')
        } else if (scrollTop <= navTop && isFixed) {
            isFixed = 0
            $nav.removeClass('subnav-fixed')
        }
    }
})

$(function () {
    $.datepicker.regional['ru'] = {
        closeText:'Закрыть',
        prevText:'&#x3c;Пред',
        nextText:'След&#x3e;',
        currentText:'Сегодня',
        monthNames:['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        monthNamesShort:['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
            'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
        dayNames:['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'],
        dayNamesShort:['вск', 'пнд', 'втр', 'срд', 'чтв', 'птн', 'сбт'],
        dayNamesMin:['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        dateFormat:"yy-mm-dd",
        firstDay:1,
        isRTL:false,
        onSelect:function (selectedDate) {
            console.log(this.id)
            if (this.id == 'date') {
                window.location = '?date=' + selectedDate
                return
            }
            var option = this.id.split('__')[1] == "gte" ? "minDate" : "maxDate",
                instance = $(this).data("datepicker"),
                date = $.datepicker.parseDate(
                    instance.settings.dateFormat ||
                        $.datepicker._defaults.dateFormat,
                    selectedDate, instance.settings);
            dates.not(this).datepicker("option", option, date);
        }
    };
    $.datepicker.setDefaults($.datepicker.regional['ru']);
    var dates = $('[type=date],[name*="date"]').datepicker();
})

$(function () {
    $('.form-add').click(function (e) {
        var prefix = $(this).data('prefix')
        var node = $('#' + prefix + '-__prefix__').clone()
        var total = $('#id_' + prefix + '-TOTAL_FORMS') //0
        var initial = $('#id_' + prefix + '-INITIAL_FORMS') //0
        var id = prefix + '-' + total.val()
        $(node).attr('id', id).html($(node).html().replace(/__prefix__/g, total.attr('value')))
        $('div.DELETE', node).remove()

        var menu = $('<li><a href="#__prefix__" data-toggle="tab"><i class="icon-"></i><span></span></a></li>'
            .replace(/__prefix__/g, total.attr('value')))
        $(menu).addClass(prefix[0].toUpperCase() + prefix.slice(1))
        $('span', menu).text($(this).attr('title'))

        var del = $('<i title="Удалить" class="icon-trash"></i>')
        $('span', menu).after(del)

        $('li.' + prefix[0].toUpperCase() + prefix.slice(1)).last().after(menu)
        $(node).appendTo('.tabbable .tab-content')
        $('a', menu).attr('href', '#' + id).removeClass('form-add')
            .data('toggle', 'tab').tab('show')
            .click(function (e) {
                $(this).tab('show')
            });
        $(del).click(function (e) {
            $(menu).remove()
            $(node).remove()
            $('.tabbable ul.nav li:first a').tab('show')
            $(total).val(parseInt($(total).val()) - 1)
        })
        $(total).val(parseInt($(total).val()) + 1)
    })
})

$(function () {
    $('tr.Bill i.icon-zoom-in').click(function (e) {
        var i = $(this).parent().parent().data('opers')
        $(this).toggleClass('zoom')
        $('#' + i).toggle('blind', null, 500)
    })

    $('th i.icon-zoom-in').click(function (e) {
        var table = $(this).parents('table')
        var tbodys = $(table).find('tbody.opers')

        var icons = $('tr.doc i.icon-zoom-in', table)
        if ($(this).hasClass('zoom')) {
            $(tbodys).hide('blind', null, 500)
            $(icons).removeClass('zoom')
        }
        else {
            $(tbodys).show('blind', null, 500)
            $(icons).addClass('zoom')
        }

        $(this).toggleClass('zoom')
    })
})

$(function () {
    var options = {
        symbol:"р",
        decimal:",",
        thousand:" ",
        precision:2,
        format:"%v <span class='ruble rel'>%s<span class='dot dborder'>.</span></span>"
    };

    $('span.money').each(function (id, n) {
        var text = accounting.formatMoney($(n).text().replace(',', '.'), options)
        $(n).html(text)
    })
})
$(function () {
    $('[rel="tooltip"]').tooltip()
    $('[rel="popover"]').popover()
})
$(function () {
    var color_select = function (select, val) {
        $(select).removeClass('bc-red bc-yellow bc-brown bc-light bc-white')
        if (val == 0) {
            $(select).addClass('bc-red')
        }
        if (val == 1) {
            $(select).addClass('bc-yellow')
        }
        if (val == 2) {
            $(select).addClass('bc-brown')
        }
        if (val == 3) {
            $(select).addClass('bc-light')
        }
        if (val == 4) {
            $(select).addClass('bc-white')
        }
    }
    var select = $('#id_color')
    var val = parseInt($(select).val())
    color_select(select, val)
    if (!val)
        $('div.ctype').hide()
    $(select).change(function () {
        var val = parseInt($(this).val())
        if (val)
            $('div.ctype').show()
        else
            $('div.ctype').hide()
        color_select(this, val)
    })
})

$(function () {
    $('[name=agent]').change(function (e) {
        var val = $(this).val()
        var a = $(this).parent('.input-append').find('a')
        if (val)
            $(a).attr('href', "/Контрагент/val/".replace('val', val))
        else
            $(a).removeAttr('href')
    })
})