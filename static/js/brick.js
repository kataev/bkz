/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
"use strict";
$(function () {
    $('#brick-select-buttons').on('click','input',function(e){ e.stopPropagation()})
    $('#brick-select-buttons').on('toggle','a', function (e) {
        $('input',this).trigger('click')
        var data = $(e.delegateTarget).serializeArray()
        var filter = _(data).chain().pluck('value').reduce(function(m,n){ return m+'.'+n},' ').value()
        var nodes = $('#Bricks tbody tr').hide().filter(filter).show()
        if (filter==' ') $('a', e.delegateTarget).removeClass('active');
        var tf = $('#Bricks tfoot th');
        var names = $('a.active', e.delegateTarget).text().trim()
        if (tf) {
            $(tf[0]).html(names)
            _(tf.slice(1)).each(function (node) { node.innerHTML = 0 })
            _(nodes).each(function (node, m) {
                $('td', node).slice(1).each(function (id, td) {
                    $(tf[id + 1]).text(parseInt(tf[id + 1].innerHTML) + parseInt(td.innerHTML))
                })
            })
        }
    })
})

function Filter(css){
    if (!css) return ' ';
    var color = String(css.match(/bc-\w{3,}/))
    var mark = parseInt(css.match(/mark-\d{3,}/)[0].replace('mark-',''))
    var view = String(css.match(/v-\w+/))
    var weight = String(css.match(/w-\w+/))
    var base = '.'+color+'.'+view+'.'+weight
    var defect = String(css.match(/d-\w+/))
    if (defect != 'd-g20') base+='.d-lux';
    return base
}

$(function () {
    $('.brick-select').on('click','a.close',function (e) {
        var target = e.delegateTarget
        $('>span',target).attr('class','uneditable-input input-large').removeAttr('title')
            .children('span').text('Выберете кирпич')
        $('input',target).val(null)
    })

    $('.brick-select').on('click','a.btn',function(e){
        var input = $('input', e.delegateTarget)
        var val = $(input).val()
        if (val) $('#brick-'+val+' input').attr('checked',true);
        $('#brick-select').data('target',e.delegateTarget)
        $('#brick-select').data('val',val)
        val = $('#'+input.attr('id')+'_from').val()
        var filter = Filter($('#brick-'+val).attr('class'))
        $('#Bricks tbody tr').hide().filter(filter).show()
    })

    $('#brick-select').on('click','tr',function(e){
        var target = $(e.delegateTarget).data('target')
        $('input:radio',this).attr('checked',true)
        $('>span',target).attr('class','uneditable-input input-large '+$(this).attr('class'))
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