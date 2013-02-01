/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
"use strict";
$('.carousel').carousel()
$('.collapse').collapse()
$('#navbar').scrollspy()

function css_to_dict(prefix, val, from) {
    var css = $('#brick-' + val).attr('class')
    var brick = {}

    if (!from) return ' ';

    brick.color = String(css.match(/bc-\w{3,}/))
    brick.mark = parseInt(css.match(/mark-\d{3,}/)[0].replace('mark-', ''))
    brick.view = String(css.match(/v-\w+/))
    brick.weight = String(css.match(/w-\w+/))
    brick.defect = String(css.match(/d-\w+/))

    var base = '.' + brick.color + '.' + brick.weight
//    if (brick.defect != 'd-g20') base+='.d-lux';
    var marks = [100, 125, 150, 175, 200, 250, 300]
    if (prefix == 'sorting') {
        var t = ''
        for (var i in marks) {
            if (marks[i] <= brick.mark) {
                t += ' .mark-' + marks[i] + base + ','
            }
        }
        base = t.slice(0, -1)
    }
    return base
}


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
    $('fieldset.Sold').on('change', 'input[name*="tara"],input[name*="brick"]', function (e) {
        var fieldset = $(e.delegateTarget)
        var brick = fieldset.find('input[name*="brick"]:last')
        var tara = fieldset.find('input[name*="tara"]').val()
        var checkbox = fieldset.find('input[name*="tara-calculate"]')
        if (checkbox.prop('checked') && brick.val() && tara) {
            var css = brick.parent().find('span').attr('class')
            var factor = bricks_per_tara(css)
            fieldset.find('input[name*="amount"]').val(factor * tara)
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

    var $bricks = $('#bricks') //Таблица с кирпичами 
    var $brickselect = $('#brickselect') //Таблица с кирпичами
    var $brickfade = $('#brickfade') // Див с кирпичами
    var $brickshow = $('#brickshow') // Див с кирпичами

    $brickselect.on('click', 'input', function (e) {
            var target = $(e.delegateTarget).data('target')
            var tr = $(this).parent().parent()
            $(target).find('>span').attr('class', 'uneditable-input ' + $(tr).attr('class'))
                .children('span').text($(tr).find('label').text().trim())
            $(target).find('input[type=hidden]').val($(this).val())
        })

    // Инпуты кирпича
    $('.brickselect').each(function () {
        var val = $('input[type=hidden]', this).val()
        if (!val) return;
        var tr = $brickselect.find('#brick-' + val)
        $('>span', this).attr('class', 'uneditable-input ' + tr.attr('class'))
            .attr('title', 'Остаток: ' + tr.find('.name').text().trim())
            .children('span').text(tr.find('.name').text().trim())
    })
        .on('click', 'a.close', function (e) {
            //Сброс значений
            var target = e.delegateTarget
            $(target).find('>span').attr('class', 'uneditable-input ').removeAttr('title')
                .children('span').text('Выберете кирпич')
            $('input[type=hidden]', target).val(null)
        })
        .on('click', 'a.btn', function (e) {
            //Выбор кирпича
            $brickfade.hide()
            $brickshow.show()
            var input = $('input[type=hidden]', e.delegateTarget)
            var val = $(input).val()
            if (val) $('#brick-' + val).find('input').attr('checked', true);
            else $brickselect.find('input').attr('checked', false);
            $brickselect.data('target', e.delegateTarget)
            var name = $(input).attr('name').split('-')
            var prefix = name[0] || ''
            name = name[name.length > 0 ? name.length-1 : 0]
            if (prefix.indexOf('solds') >= 0)  {
                if (name == 'brick_from') var from = 0;
                if (name == 'brick') var from = $('#' + input.attr('id') + '_from').val();
            }
            if (prefix.indexOf('sorting') >= 0) var from = $('input[name=brick]').val();
            var filter = css_to_dict(prefix, val, from)
            if (filter.length > 1)
            $brickselect.find('tbody tr').hide().filter(filter).show()
            else
            $brickselect.find('tbody tr').show()
        })
        $brickshow.on('click', 'a.back', function (e) {
            $brickfade.show()
            $brickshow.hide()
        })

    //Фильтер кирпича по кнопкам
    $('#brickselect-buttons').on('submit', function (e) {
        e.preventDefault()
        var data = $(this).serializeArray()
        var $rows = $bricks.find('tbody tr').hide()
        var dict = {}
        for (var d in data) {
            var ar = dict[data[d].name] || []
            ar.push(data[d].value)
            dict[data[d].name] = ar
        }
        for (var d in dict){
            $rows = $rows.filter(function(i,row){
                var a
                for (var i in dict[d]){ a = a || $(row).hasClass(dict[d][i]) }
                return a
            })
        }
        var totals = []
        $rows.show().each(function(i,node) {
             $(node).find('td').slice(1).each(function(i,node){totals[i]=(totals[i] || 0) + parseInt(this.innerHTML)})
        })
        $bricks.find('tfoot tr').find('th').slice(1).each(function(i,node){node.innerHTML = totals[i]})

    }).on('click','input',function(e){
            var name = $(this).attr('name')
            var span = $(e.delegateTarget).find('a[href="#'+name+'"]').find('span.label')
            if ($(this).prop('checked')) $(span).text(parseInt($(span).text())+1).addClass('label-warning')
            else $(span).text(parseInt($(span).text())-1)
            if (!parseInt($(span).text())) $(span).removeClass('label-warning')
        }).on('reset',function(e){
            $(this).find('span.label').removeClass('label-warning').text(0)
        })
   
})