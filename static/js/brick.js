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

function filter(css){
    var color = String(css.match(/bc-\w{3,}/))
    var mark = parseInt(css.match(/mark-\d{3,}/)[0].replace('mark-',''))
    var view = String(css.match(/v-\w+/))
    var weight = String(css.match(/w-\w+/))
    var base = color+'.'+view+'.'+weight
    var defect = String(css.match(/d-\w+/))
    if (defect != 'd-g20') base+='.d-lux';
    return base
}

$(function () {
    $('.brick-select').on('click','a.close',function (e) {
        var target = e.delegateTarget
        $('>span',target).attr('class','uneditable-input').removeAttr('title')
            .children('span').text('Выберете кирпич')
        $('input',target).val(null)
    })

    $('.brick-select').on('click','a.btn',function(e){
        var val = $('input', e.delegateTarget).val()
        if (val) $('#brick-'+val+' input').attr('checked',true);
        $('#brick-select').data('target',e.delegateTarget)
        $('#brick-select').data('val',val)
    })

    $('#brick-select').on('click','tr',function(e){
        var target = $(e.delegateTarget).data('target')
        $('input:radio',this).attr('checked',true)
        $('>span',target).attr('class','uneditable-input '+$(this).attr('class'))
            .attr('title','Остаток: '+$('.total',this).text().trim())
            .children('span').text($('.name',this).text().trim())
        $('input',target).val($('input:radio',this).val())
    })
    $('#brick-select').on('shown',function(e){
        var val = $(this).data('val')
        if (val) {
            window.location.hash = 'brick-'+val
        }
    })
})