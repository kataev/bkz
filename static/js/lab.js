$(function () {
    $('td.create .form-add').click(function (e) {
        var prefix = $(this).data('prefix')
        var node = $('#' + prefix + '-__prefix__').clone(true).appendTo()
        var total = $('#id_' + prefix + '-TOTAL_FORMS') //0
        var initial = $('#id_' + prefix + '-INITIAL_FORMS') //0
        var id = prefix + '-' + total.val()
        var v = total.attr('value')
        var rep = function (index, value) { if (value) return value.replace(/__prefix__/g, v) }
        $(node).attr('id', rep)
        $('input, select', node).attr('name', rep).attr('id', rep)
        $('label[for]', node).attr('for', rep)
        $('div.modal', node).attr('id', rep)
        $('button[data-toggle="modal"]', node).attr('data-target', rep)

        $(total).val(parseInt($(total).val()) + 1)
    })


})
