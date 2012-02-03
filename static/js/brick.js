/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */
$(function () {
    $('a', '#brick-select').on('toggle', function (e) {
        if (!$(this).attr('href')){
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
        _(tf.slice(2)).each(function (node,id) { node.innerHTML = 0 })
        _(nodes).each(function (node,m) {
            $('td', node).slice(2).each(function (id,td) {
//                if (id <= 1) { return }
                $(tf[id+2]).html(parseInt(tf[id+2].innerHTML) + parseInt(td.innerHTML))
            })
        })
    })

})