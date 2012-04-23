/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
"use strict";
$(function () {
    $('a', '#brick-select-buttons').on('toggle', function (e) {
        if (!$(this).attr('href')) {
            $(this).parents('.subnav').find('a.active').removeClass('active')
        }
        if ($(this).attr('rel')) {
            $(this).parents('.subnav').find('[rel='+$(this).attr('rel')+']').not(this).removeClass('active')
        }
        var active = $('a.active', '#brick-select-buttons')
        var names = _(active).reduce(function (m, n) {
            return m + ' ' + $(n).html()
        }, '')
        var filter = _(active).reduce( function (m, n) { return m + $(n).attr('href').replace('#', '.') }, '').replace('#', '.');
        var nodes
        if (filter.length == 0) {
            nodes = $('tr', '#Bricks tbody').show()
            $('a', '#brick-select-buttons').removeClass('active')
        } else {
            $('tr', '#Bricks tbody').hide()
            nodes = $(filter, '#Bricks tbody').show()
        }
        var tf = $('th', '#Bricks tfoot');
        if (tf) {
            $(tf[0]).html(names)
            _(tf.slice(1)).each(function (node, id) {
                node.innerHTML = 0
            })

            _(nodes).each(function (node, m) {
                $('td', node).slice(1).each(function (id, td) {
                    $(tf[id + 1]).text(parseInt(tf[id + 1].innerHTML) + parseInt(td.innerHTML))
                })
            })
        }
    })
})


$(function () {
    $('span a.close').click(function (e) {
        var input = $(this).parent()
        var span = $(input).children('span')

        $(span).text('Выберете кирпич')
        $(input).attr('class','uneditable-input span')
        $(input).attr('title','')
        $('#'+$(input).attr('id').replace('_span','')).val(null)
    })

    $('body').on('click.modal.data-api', '[data-toggle="brick-select"]', function (e) {
        var $this = $(this), href
            , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
            , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

        e.preventDefault()
        $($target).data('button', $(e.target).parent())
        $target.modal(option)
    })
    var modal = $('#brick-select')
    $('tr', modal).click(function (e) {
        var button = $(modal).data('button')
        var input = $(button).data('input')

        $('#' + input).val($('input', this).val())

        $('#' + input + '_span span').html($('td.name', this).text().trim())
        $('#' + input + '_span').attr('title','Остаток: '+$('td.total', this).text().trim())
        $('#' + input + '_span').attr('class', 'input uneditable-input ' + $(this).attr('class'))
        $('#' + input).change()
    })
    var marks = [100,125,150,175,200,250,300,9000]
    $(modal).on('show', function () {
        var button = $(modal).data('button')
        var input = $(button).data('input')
        var val = $('#' + input).val()
        var model = $('#'+ input).data('model')
        if (val) {
            $('[value=' + val + ']', modal).attr('checked', 'checked')
        }
        else {
            $('[value]', modal).removeAttr('checked')
        }
        var from = $('#'+$('#'+input).data('brick_from'))
        if (from.val()) {
            var css = $('#'+from.attr('id')+'_span').attr('class')
            var color = String(css.match(/bc-\w{3,}/))
            var mark = parseInt(css.match(/mark-\d{3,}/)[0].replace('mark-',''))
            var view = String(css.match(/v-\w+/))
            var weight = String(css.match(/w-\w+/))
            var base = color+'.'+view+'.'+weight
            var defect = String(css.match(/d-\w+/))
//            defect={u'': u'd-lux', u'd-<20': u'd-l20', u'd->20': u'd-g20'},
            if (defect != 'd-g20') base+='.d-lux';
            if (model == 'Sold') {
                var sel = _(marks).chain().filter(function(i){ return defect == 'd-lux' ? i < mark : i <= mark })
                    .reduce(function(memo,num){ return memo += ', tr.'+base+'.mark-'+num; }, '').value().slice(2)
            }
            $('tr',modal).not(sel).hide()
            console.log(sel)
        }
        else $('tr',modal).show()
    })
})