/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
"use strict";
$(function () {
    $('.form-add').click(function (e) {
        var prefix = $(this).data('prefix')
        var append_to = $(this).data('append')
        var place_to = $(this).data('place') || $(this).parents('ul')
        if (!append_to) throw "Куда приклеплять?!"
        var node = $('#' + prefix + '-__prefix__').clone(true).appendTo(append_to)
        var total = $('#id_' + prefix + '-TOTAL_FORMS') //0
        var initial = $('#id_' + prefix + '-INITIAL_FORMS') //0
        var id = prefix + '-' + total.val()
        var v = total.attr('value')
        var rep = function (index, value) { if (value) return value.replace(/__prefix__/g, v) }
        $(node).attr('id', rep)
        $('input, select', node).attr('name', rep).attr('id', rep)
        $('label[for]', node).attr('for', rep)
        $('*', node).attr('id', rep)
        var menu = $('<li><a href="#__prefix__" data-toggle="tab"><span></span></a></li>'
            .replace(/__prefix__/g, total.attr('value')))
        $(menu).addClass(prefix[0].toUpperCase() + prefix.slice(1)).appendTo(place_to)
        $('span', menu).text($('legend',node).text())


        $(total).val(parseInt($(total).val()) + 1)
        tara_amount()
        $('a', menu).attr('href', '#' + id).removeClass('form-add')
    })

//    $('nav.nav-list.form-nav').on('click.tab.data-api','[data-toggle="tab"',function(e){
//        e.preventDefault()
//        $(this).tab('show')
//    })
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
    $('[rel="popover"]').popover()
    $(".collapse").collapse()
})

//Подсветка цветов селекта в редактировании кирпича
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
    $('[name=agent],[name=seller]').change(function (e) {
        var val = $(this).val()
        var div = $(this).parent()
        var a = $(div).children("a")
        var i = $(a).children("i")
        var href = $(div).attr('href')
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

function bricks_per_tara(cl) {
    var f = function (str) {
        return cl.indexOf(str) >= 0
    }
//  width={1: u'single', 1.4: u'thickened', 0: u'double', 0.8: u'euro'},
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
    $('fieldset').on('change', 'input[name*="tara"],input[name*="brick"]', function (e) {
        var fieldset = $(e.delegateTarget)
        var brick = $('.brick-select.brick input', fieldset)
        var tara = $('input[name*="tara"]', fieldset)
        var checkbox = $('input[name="tara-calculate"]', fieldset)
        if (checkbox.val() && brick.val() && tara.val()) {
            var css = $('.brick-select.brick > span', fieldset).attr('class')
            var factor = bricks_per_tara(css)
            $('input[name*="amount"]', fieldset).val(factor * tara.val())
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
        url += '/' + name + '/' + window.location.search
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
$('[name="month"],[name*="month"]').change(function (e) {
    var year = $(':selected', this).parent().attr('label')
    $(this).parents('form').find('[name="'+($(this).attr('name').replace('month','year'))+'"]').val(year)
})

$('form.filter').submit(function (e) {
    e.preventDefault()
    var param = jQuery.param($(this).serializeArray().filter(function (e) { return e.value }))
    window.location.search = '?' + param
})

function avg_on_input(input,to_fixed){
    var v = $(input).val().split('/').map(function(v){return v.replace(',','.')})
    return (v.reduce(function(m,v){return m+parseFloat(v) },0)/v.length).toFixed(to_fixed || 2)
}

$('.SlashSeparatedFloatField').each(function(e){
    $(this).wrap($('<div>').addClass('input-append').attr('title','Среднее арифметическое'))
    var addon = $('<span>').addClass('add-on').text(avg_on_input(this)).insertAfter(this)
    $(this).change(function(e){ $(addon).text(avg_on_input(this)) })
})