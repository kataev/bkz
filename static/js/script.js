/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
"use strict";
$('.carousel').carousel()
$('.collapse').collapse()
$('#navbar').scrollspy()

$(function () {
    $('select[name*="defect"]').change(function(e){
        var $cause = $('#'+$(this).attr('id').replace('defect','cause')).parent()
        if ($(this).val() == 'gost')$cause.hide();
         else $cause.show();
    })

    $('.form-add').click(function (e) {
        e.preventDefault()
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

        $(node).on('click','a.delete',function(){
            $(total).val(parseInt($(total).val()) - 1)
            $(node).remove()
        })

        $(total).val(parseInt($(total).val()) + 1)
        tara_amount()
        $('a', menu).attr('href', '#' + id).removeClass('form-add')
    })

    $('.delete').click(function(e){
        e.preventDefault()
        var dl = $($(this).attr('href')).find('[name*="DELETE"]')
        dl.prop('checked',!dl.prop('checked'))
        $(this).toggleClass('btn-warning').toggleClass('btn-danger')
        $(this).find('i').toggleClass('icon-remove').toggleClass('icon-trash')
    })
})

$(function () {
    $('tr[data-opers] i.icon-zoom-in').click(function () {
        var i = $(this).parent().parent().data('opers')
        $(this).toggleClass('zoom')
        $('#' + i).toggle('blind', null, 500)
    })

    $('th i.icon-zoom-in').click(function () {
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

    var $messages = $('#messages').popover('show')

    setTimeout(function(e){$messages.popover('hide')},10000)
    if ($.mask){
    if ($("input[name*='form']").val())
    $("input[name*='inn']").mask('999 999 999 999')
    else
    $("input[name*='inn']").mask('99 99 99 99 99')
    $("input[name*='kpp']").mask('999 999 999')
    }
})

//Подсветка цветов селекта в редактировании кирпича
$(function () {
    var color_select = function (select, val) {
        var $select = $(select)
        $select.removeClass('bc-red bc-yellow bc-brown bc-light bc-white')
        if (val == 0) $select.addClass('bc-red');
        if (val == 1) $select.addClass('bc-yellow');
        if (val == 2) $select.addClass('bc-brown');
        if (val == 3) $select.addClass('bc-light');
        if (val == 4) $select.addClass('bc-white');
    }
    var select = $('#id_color')
    var val = parseInt($(select).val())
    color_select(select, val)
    if (!val)
        $('div.ctype').hide()
    $(select).change(function () {
        var val = parseInt($(this).val())
        if (val) $('div.ctype').show();
        else $('div.ctype').hide();
        color_select(this, val)
    })

    $('fieldset').on('click','a.show',function(e){
        e.preventDefault()
        $(e.delegateTarget).find('.row:hidden:first').show()
    })
})

$(function () {
    $('[name=agent],[name=seller]').change(function () {
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
        var brick = $('.brickselect.brick input', fieldset)
        var tara = $('input[name*="tara"]', fieldset)
        var checkbox = $('input[name="tara-calculate"]', fieldset)
        if (checkbox.val() && brick.val() && tara.val()) {
            var css = $('.brickselect.brick > span', fieldset).attr('class')
            var factor = bricks_per_tara(css)
            $('input[name*="amount"]', fieldset).val(factor * tara.val())
        }
    })
}
$(tara_amount)

$(function () {
    $("#Bricks td[rel='popover']").click(function () {
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
        $(this).data('popover').$tip.on('click.close', $.proxy(function () {
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
            }).error(function () {
                $('<p><span class="label label-important"><i class="icon-warning-sign"></i>Что-то пошло не так</span></p>')
                    .addClass('alert alert-error')
                    .appendTo($(this).data('popover').$tip.find('.popover-content').empty())
            })
    })
})
$('[name="month"],[name*="month"]').change(function () {
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

$('.SlashSeparatedFloatField').each(function(){
    $(this).wrap($('<div>').addClass('input-append').attr('title','Среднее арифметическое'))
    var addon = $('<span>').addClass('add-on').text(avg_on_input(this)).insertAfter(this)
    $(this).change(function(){ $(addon).text(avg_on_input(this)) })
})

function get_area_and_volume(id,size) {
    var val = $.map(size.split('x'),function(v){return parseFloat(v)})
    var s = val[1]*val[id.indexOf('pressure') >= 0 ? 0 : 2 ]/1000
    if (id.indexOf('pressure') >= 0) 
        s-=0.243;
    else 
        s*=val[2]*2
    return [s,val[0] * val[1] * val[2] / Math.pow(100*10,3)]
}


$(function(){
    $("input[name*='size'][type='text']").mask('999.9 x 999.9 x 99.9').change(function(e){
        var id = $(this).attr('id')
        var size = $(this).val()
        var q = get_area_and_volume(id,size)
        $('#'+id.replace('size','area')).val(q[0]).attr('title','Объем м³: '+q[1])
        $('#'+id.replace('size','readings')).change()
    })
    $("input[name*='readings']").change(function(e){
        var id = $(this).attr('id')
        var s = $('#'+id.replace('readings','area')).val()
        var r = $(this).val()
        if (s*r) {
            var v = 0
            if (id.indexOf('pressure') >= 0) {
                //Сжатие
                v = (r/s).toFixed(2)
                if ($('#width').val() > 1)
                    v=(v * 1.2).toFixed(2)
            }
            else {
                //Изгиб
                v = (192.498*r*0.6/s).toFixed(2)
            }
            $('#'+id.replace('readings','value')).val(v)
        }
    })

    $('#form').on('change',"input[name='volume'],input[name='weight']",function(e){
        var id = $(e.delegateTarget).find('input[name="volume"]:checked').val()
        if (!id) return;
        var size = $('#id_'+id+'-size').val()
        var w = $('#id_weight').val()
        if (size && w) {
            var vol = get_area_and_volume(id,size)[1]
            var dens = (w/vol).toFixed(2)
            $('#id_density').val(dens)
            var cad = ''
            if (dens <= 800) cad = 0.8;
            if (dens >= 801 && dens <= 1000) cad = 1.0;
            if (dens >= 1001 && dens <= 1200) cad = 1.2;
            if (dens >= 1201 && dens <= 1400) cad = 1.4;
            if (dens >= 1400) cad = 2.0;
            $('#id_cad').val(cad)
        }
    })
})