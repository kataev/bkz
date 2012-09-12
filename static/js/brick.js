/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
"use strict";

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
    $('.brickselect').each(function (id) {
        var val = $('input[type=hidden]', this).val()
        if (val) {
            var tr = $('#brick-' + val)
            $('>span', this).attr('class', 'uneditable-input ' + $(tr).attr('class'))
                .attr('title', 'Остаток: ' + $('.total', tr).text().trim())
                .children('span').text($('.name', tr).text().trim())
        }
    })
        .on('click', 'a.close', function (e) {
            //Сброс значений
            var target = e.delegateTarget
            $('>span', target).attr('class', 'uneditable-input ').removeAttr('title')
                .children('span').text('Выберете кирпич')
            $('input[type=hidden]', target).val(null)
        })
        .on('click', 'a.btn', function (e) {
            //Выбор кирпича
            var input = $('input[type=hidden]', e.delegateTarget)
            var val = $(input).val()
            if (val) $('#brick-' + val + ' input').attr('checked', true);
            $('#brickselect').data('target', e.delegateTarget).data('val', val)

            var name = $(input).attr('name').split('_')
            if (name.length > 1) {
                var prefix = name[0]
                name = name[name.length]
            }
            else {
                var prefix = ''
                name = name[0]
            }
            if (prefix == 'solds') {
                if (name == 'brick_from') {
                    var from = 0
                }
                if (name == 'brick') {
                    var from = $('#' + input.attr('id') + '_from').val()
                }
            }
            if (prefix == 'sorting') {
                var from = $('input[name=brick]').val()
            }
            var filter = css_to_dict(prefix, val, from)
            $('#Bricks').find('tbody tr').hide().filter(filter).show()
            $('#brickselect-fade').hide()
            $('#brickselect').show()
        })

    $('#Bricks').find('tbody tr').map(function (e, tr) {
        var td = $('td', tr).slice(1).map(function (id, td) {
            return parseInt(td.innerHTML)
        })
        return {'css':$(tr).attr('class'), 'node':tr, 'td':td}
    })

    $('#brick-select-buttons').on('submit', function (e) {
        e.preventDefault()
        var data = $(e.delegateTarget).serializeArray()

    })
        .on('click', 'input', function (e) {
            e.stopPropagation()
        })
        .on('click', 'a', function (e) {
            //Фильтр при нажатии на кнопки
            if (!$('input', this).trigger('click').length) {
                return
            }
            var data = $(e.delegateTarget).serializeArray()
            var filter = _(data).chain().pluck('value').reduce(function (m, n) {
                return m + '.' + n
            }, ' ').value()
            var nodes = $('#Bricks tbody tr').hide().filter(filter).show()
            if (filter == ' ') $('a', e.delegateTarget).removeClass('active');
            var tf = $('#Bricks').find('tfoot th');
            var names = $('a.active', e.delegateTarget).text().trim()
            if (tf) {
                $(tf[0]).html(names)
                _(tf.slice(1)).each(function (node) {
                    node.innerHTML = 0
                })
                _(nodes).each(function (node) {
                    $('td', node).slice(1).each(function (id, td) {
                        $(tf[id + 1]).text(parseInt(tf[id + 1].innerHTML) + parseInt(td.innerHTML))
                    })
                })
            }
        })
})


$(function () {
    $('#brickselect').on('click', 'a', function () {
        $('#brickselect-fade').show()
        $(this).hide()
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