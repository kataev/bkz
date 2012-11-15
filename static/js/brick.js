/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
'use strict';

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
    var $brickselect = $('#brickselect') //Кнопки для фильтрации
    var $bricks = $('#Bricks')// Таблица с кирпичами
    var $brickfade = $('#brickfade') // Див с кирпичами

    // Инпуты кирпича
    $('.brickselect').each(function () {
        var val = $('input[type=hidden]', this).val()
        if (!val) return;
        var tr = $bricks.find('#brick-' + val)
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
            $brickselect.show()
            var input = $('input[type=hidden]', e.delegateTarget)
            var val = $(input).val()
            if (val) $('#brick-' + val).find('input').attr('checked', true);
            $brickselect.data('target', e.delegateTarget).data('val', val)
            var name = $(input).attr('name').split('_')
            var prefix = name[0] || ''
            name = name[name.length > 0 ? name.length : 0]
            if (prefix == 'solds') {
                if (name == 'brick_from') var from = 0;
                if (name == 'brick') var from = $('#' + input.attr('id') + '_from').val();
            }
            if (prefix == 'sorting') var from = $('input[name=brick]').val();
            var filter = css_to_dict(prefix, val, from)
            $bricks.find('tbody tr').hide().filter(filter).show()
        })

    $bricks.find('tbody tr').map(function (e, tr) {
        var td = $('td', tr).slice(1).map(function (id, td) { return parseInt(td.innerHTML)})
        return {'css':$(tr).attr('class'), 'node':tr, 'td':td}
    })

    var $tfoot = $bricks.find('tfoot tr')
    //Фильтер кирпича по кнопкам
    $('#brick-select-buttons').on('submit', function (e) {
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
//        .on('click', 'a', function (e) {
//            //Фильтр при нажатии на кнопки
//            if (!$('input', this).trigger('click').length) return;
//            var data = $(e.delegateTarget).serializeArray()
//            var filter = _(data).chain().pluck('value').reduce(function (m, n) { return m + '.' + n }, ' ').value()
//            var nodes = $bricks.find('tbody tr').hide().filter(filter).show()
//            if (filter == ' ') $('a', e.delegateTarget).removeClass('active');
//            var tf = $bricks.find('tfoot th');
//            var names = $('a.active', e.delegateTarget).text().trim()
//            if (tf) {
//                $(tf[0]).html(names)
//                _(tf.slice(1)).each(function (node) {
//                    node.innerHTML = 0
//                })
//                _(nodes).each(function (node) {
//                    $('td', node).slice(1).each(function (id, td) {
//                        $(tf[id + 1]).text(parseInt(tf[id + 1].innerHTML) + parseInt(td.innerHTML))
//                    })
//                })
//            }
//        })

    $brickselect.on('click', 'a', function (e) {
        $brickfade.show()
        $brickselect.hide()
    })
        .on('click', 'tr', function (e) {
            var target = $(e.delegateTarget).data('target')
            $('input:radio', this).attr('checked', true)
            $('>span', target).attr('class', 'uneditable-input ' + $(this).attr('class'))
                .attr('title', 'Остаток: ' + $('.total', this).text().trim())
                .children('span').text($('.name', this).text().trim())
            $('input[type=hidden]', target).val($('input:radio', this).val())
        })
        .on('shown', function () {
            var val = $(this).data('val')
            if (val) {
                window.location.hash = 'brick-' + val
            }
        })
})