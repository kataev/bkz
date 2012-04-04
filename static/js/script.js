/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
"use strict";
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
        tara_amount()
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

        var icons = $('td i.icon-zoom-in', table)
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
//    $('[rel="popover"]').popover()
    $(".collapse").collapse()
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
        var input = $(this).parent(".input-append")
        var a = $(input).find("a")
        var i = $(input).find("i")
        if (val) {
            $(a).attr('href', href + val + "/")
            $(a).attr('title', "Редактировать выбранного контрагента")
            $(i).attr('class', "icon-info-sign")
        }
        else {
            $(a).attr('href', href)
            $(a).attr('title', "Создать контрагента")
            $(i).attr('class', "icon-plus-sign")
        }
    })
})

function tara(cl) {
    var f = function (str) {
        return cl.indexOf(str) >= 0
    }
//  weight={1: u'single', 1.4: u'thickened', 0: u'double', 0.8: u'euro'},
//  view={u'Л': u'facial', u'Р': u'common'},
    if (f('double')) {
        return 160
    }
    if (f('bc-yellow')) {
        if (f('thickened')) {
            return 192
        }
        else if (f('single')) {
            return 264
        }
    }

    if (f('common')) {
        if (f('thickened')) {
            return 288
        }
        else if (f('single')) {
            return 352
        }
        else if (f('euro')) {
            return 352
        }
    } else {
        if (f('thickened')) {
            return 192
        }
        else if (f('single')) {
            return 264
        }
        else if (f('euro')) {
            return 256
        }
    }

}

function tara_amount() {
    $('input[name*="tara"],input[name*="brick"],input[name*="brick_to"]').change(function (e) {
        var id = $(this).attr('id')
        var s = id.split('-')
        var form = id.split(s[s.length - 1])[0]
        var val = parseInt($('#' + form + 'tara').val())
        var brick = $('#' + form + 'brick').length ? $('#' + form + 'brick') : $('#' + form + 'brick_to')
        var checkbox = $('#' + form + 'tara_checkbox')
        if ($(checkbox).attr('checked') && $(brick).val() && val) {
            var factor = tara($('#' + $(brick).attr('id') + '_span').attr('class'))
            var amount = $('#' + form + 'amount')
            $(amount).val(factor * val)
        }
    })
}
$(tara_amount)

$(function () {
    $("td[rel='popover']").click(function (e) {
        if (parseInt($(this).text()) <= 0)
            return
        var name = $(this).data('name')
        if (name == 'total' || name == 'begin')
            return
        $(this).popover()
        var tr = $(this).parent('tr')
        var brick = $(tr).find('td:first').text()
        var url = $(tr).find('td:first a').attr('href')
        var css = $(tr).attr('class')
        $(this).data('popover').$element.attr('data-original-title', '<span class="' + css + '">' + brick + '</span><i class="close">&times;</i>')
        $(this).data('popover').$element.attr('data-content', '<p><img src="/static/img/loader.gif"><p><span class="label">Загрузка</span></p></p>')

        $(this).popover('show')
        $(this).data('popover').$tip.on('click.close', $.proxy(function (e) {
            $(this).popover('hide')
        }, this))
        url += '/' + name + '/2012/04/'
        $.ajax({url:url, context:this }).success(
            function (data) {
                var table = $('<table class="table table-condensed table-striped"></table>')
                    .appendTo($(this).data('popover')
                    .$tip.find('.popover-content').empty())
                var tbody = $('<tbody></tbody>').appendTo(table)
                $('<thead><tr><th>Дата</th><th>Кол-во</th></tr></thead>').appendTo(table)
                _(data).each(function (a) {
                    var tr = $('<tr></tr>').appendTo(tbody)
                    _(a).each(function (e) {
                        $('<td></td>').appendTo(tr).text(e)
                    })
                })
                var sum = _(data).reduce(function (m, v) {
                    return m + v[1]
                }, 0)
                var tfoot = $('<tfoot>').appendTo(table)
                var tr = $('<tr>').appendTo(tfoot)
                $('<th>').appendTo(tr).text('Итого:').attr('style', 'text-align:right')
                $('<td>').appendTo(tr).text(sum)
            }).error(function (e) {
                $('<p><span class="label label-important"><i class="icon-warning-sign"></i>Что-то пошло не так</span></p>')
                    .addClass('alert alert-error')
                    .appendTo($(this).data('popover').$tip.find('.popover-content').empty())
            })
    })
})