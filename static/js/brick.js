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
            else $('#Bricks').find('input').attr('checked', false);
            $bricks.data('target', e.delegateTarget)
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
            $bricks.find('tbody tr').hide().filter(filter).show()
            else
            $bricks.find('tbody tr').show()
        })
        $brickselect.on('click', 'a.back', function (e) {
            $brickfade.show()
            $brickselect.hide()
        })
        
        $bricks.on('click', 'input', function (e) {
            var target = $(e.delegateTarget).data('target')
            var tr = $(this).parent().parent()
            $(target).find('>span').attr('class', 'uneditable-input ' + $(tr).attr('class'))
                .children('span').text($(tr).find('label').text().trim())
            $(target).find('input[type=hidden]').val($(this).val())
        })

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

    
})