/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
"use strict";
$(function () {
    $('.brickselect').each(function(id){
        var val = $('input[type=hidden]', this).val()
        if (val){
            var tr = $('#brick-'+val)
            $('>span',this).attr('class','uneditable-input '+$(tr).attr('class'))
                .attr('title','Остаток: '+$('.total',tr).text().trim())
                .children('span').text($('.name',tr).text().trim())
        }
    })
    $('#brick-select-buttons').on('submit',function(e){
        e.preventDefault()
        alert('submited')
    })
    $('#brick-select-buttons').on('click','input',function(e){ e.stopPropagation()})
    $('#brick-select-buttons').on('click','a', function (e) {
        //Фильтр при нажатии на кнопки
        if (!$('input',this).trigger('click').length){return}
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

function css_to_dict(prefix,val,from){
    var css = $('#brick-'+val).attr('class')
    var brick = {}

    if (!from) return ' ';
    
    brick.color = String(css.match(/bc-\w{3,}/))
    brick.mark = parseInt(css.match(/mark-\d{3,}/)[0].replace('mark-',''))
    brick.view = String(css.match(/v-\w+/))
    brick.weight = String(css.match(/w-\w+/))
    brick.defect = String(css.match(/d-\w+/))

    var base = '.'+brick.color+'.'+brick.weight
//    if (brick.defect != 'd-g20') base+='.d-lux';
    var marks = [100,125,150,175,200,250,300]
    if (prefix == 'sorting') {
        var t = ''
        for (var i in marks){
            if (marks[i] <= brick.mark){
                t+=' .mark-'+marks[i]+base+','
            }
        }
        base = t.slice(0,-1)
    }
    console.log(arguments,css,brick,base);
    return base
}

$(function () {
    $('.brickselect').on('click','a.close',function (e) {
        //Сброс значений
        var target = e.delegateTarget
        $('>span',target).attr('class','uneditable-input ').removeAttr('title')
            .children('span').text('Выберете кирпич')
        $('input[type=hidden]',target).val(null)
    })

    $('.brickselect').on('click','a.btn',function(e){
        //Выбор кирпича
        var input = $('input[type=hidden]', e.delegateTarget)
        var val = $(input).val()
        if (val) $('#brick-'+val+' input').attr('checked',true);
        $('#brickselect').data('target',e.delegateTarget)
        $('#brickselect').data('val',val)

        var name = $(input).attr('name').split('_')
        if (name.length>1){
            var prefix = name[0]
            name = name[name.length]
        }
        else {
            var prefix = ''
            name = name[0]
        }
        if (prefix == 'solds') {
            if (name=='brick_from'){var from = 0}
            if (name=='brick'){ var from = $('#'+input.attr('id')+'_from').val() }
        }
        if (prefix == 'sorting'){
            var from = $('input[name=brick]').val()
        }
        var filter = css_to_dict(prefix,val,from)
        $('#Bricks tbody tr').hide().filter(filter).show()
        $('#brickselect-fade').hide()
        $('#brickselect').show()
    })

    $('#brickselect').on('click','a',function(e){
        $('#brickselect-fade').show()
        $('#brickselect').hide()
    })

    $('#brickselect').on('click','tr',function(e){
        var target = $(e.delegateTarget).data('target')
        $('input:radio',this).attr('checked',true)
        $('>span',target).attr('class','uneditable-input '+$(this).attr('class'))
            .attr('title','Остаток: '+$('.total',this).text().trim())
            .children('span').text($('.name',this).text().trim())
        $('input[type=hidden]',target).val($('input:radio',this).val())
    })
    $('#brickselect').on('shown',function(e){
        var val = $(this).data('val')
        if (val) {
            window.location.hash = 'brick-'+val
        }
    })
})