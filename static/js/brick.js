/*
 * User: bteam
 * Date: 02.02.12
 * Time: 16:24
 */

$('[data-widget="brick-select"]').each(function(m,node){
    console.log(m,node)
        var name = $(node).attr('name')
        var id = $(node).attr('id')

        $(node).replaceWith
});

$('body').on('click', '[data-widget="brick-select"]', function ( e ) {
    console.log(e)
})