/*
 * User: bteam
 * Date: 03.02.12
 * Time: 11:01
 */
$(function () {
    var $win = $(window)
        , $nav = $('.subnav')
        , navTop = $('.subnav').length && $('.subnav').offset().top - 40
        , isFixed = 0

    processScroll()

    $win.on('scroll', processScroll)

    function processScroll() {
        var i, scrollTop = $win.scrollTop()
        if (scrollTop >= navTop && !isFixed) {
            isFixed = 1
            $nav.addClass('subnav-fixed')
        } else if (scrollTop <= navTop && isFixed) {
            isFixed = 0
            $nav.removeClass('subnav-fixed')
        }
    }
})

$(function () {
    $("[type=date]").datepicker({"dateFormat":"yy-mm-dd"});
})

$(function () {
    $('.form-add').click(function (e,test) {
        console.log(test)
        var prefix = $(this).attr('href').slice(1)
        var node = $('#' + prefix + '-__prefix__').clone()
        var total = $('#id_'+prefix+'-TOTAL_FORMS') //0
        var initial = $('#id_'+prefix+'-INITIAL_FORMS') //0
        var id = prefix + '-' + total.val()
        $(node).attr('id', id)
        $(node).html($(node).html().replace(/__prefix__/g, total.attr('value')))
        $('div.DELETE',node).remove()
        var menu = $(this).parent().clone()

        if ($(this).data('transfer')){
            console.log('create sold from transfer')
        }

        $('a', menu).wrapInner('<span></span>')
        var del = $('<i title="Удалить" class="icon-trash"></i>')
        $('span', menu).after(del)

        $('.tabbable ul.nav li.dropdown').before(menu)
        $(node).appendTo('.tabbable .tab-content')
        $('a', menu).attr('href', '#' + id).removeClass('form-add')
            .data('toggle', 'tab').tab('show')
            .click(function (e) {
                $(this).tab('show')
            });
        $(del).click(function(e){
            $(menu).remove()
            $(node).remove()
            $('.tabbable ul.nav li:first a').tab('show')
            $(total).val(parseInt($(total).val()) - 1)
        })
        $(total).val(parseInt($(total).val()) + 1)
    })
})