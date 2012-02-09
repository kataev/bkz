/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
$(function () {
    $('a', '#brick-select').on('toggle', function (e) {
        if (!$(this).attr('href')) {
            $(this).siblings().removeClass('active')
        }
        var active = $('a.active', '#brick-select')
        var names = _(active).reduce(function (m, n) {
            return m + ' ' + $(n).html()
        }, '')
        var filter = _(active).reduce(
            function (m, n) {
                return m + $(n).attr('href').replace('#', '.')
            }, '').replace('#', '.');
        var nodes
        if (filter.length == 0) {
            nodes = $('tr', '#Bricks tbody').show()
            $('a', '#brick-select').removeClass('active')
        } else {
            $('tr', '#Bricks tbody').hide()
            nodes = $(filter, '#Bricks tbody').show()
        }

        var tf = $('th', '#Bricks tfoot');
        $(tf[0]).html(nodes.length)
        $(tf[1]).html(names)
        _(tf.slice(2)).each(function (node, id) {
            node.innerHTML = 0
        })
        _(nodes).each(function (node, m) {
            $('td', node).slice(2).each(function (id, td) {
//                if (id <= 1) { return }
                $(tf[id + 2]).html(parseInt(tf[id + 2].innerHTML) + parseInt(td.innerHTML))
            })
        })
    })
})


$(function () {
    $('body').on('click.modal.data-api', '[data-toggle="brick-select"]', function (e) {
        var $this = $(this), href
            , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
            , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

        e.preventDefault()
        $($target).data('button', e.target)
        $target.modal(option)
    })
    var modal = $('#brick-select')
    $('tr', modal).click(function (e) {
        var button = $(modal).data('button')
        var input = $(button).data('input')
        $('#'+input).val($('td:first', this).text())
        $('#'+input+'_span').html($('td', this)[1].innerHTML)
        $('#'+input+'_span').attr('class','input uneditable-input '+ $(this).attr('class'))
    })



})