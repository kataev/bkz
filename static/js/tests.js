$(function(){
    $("input[name*='size']").mask('999.9 x 999.9 x 99.9').change(function(e){
        var id = $(this).attr('id')
        var val = $.map($(this).val().split('x'),function(v){return parseFloat(v)})
        var s = val[1]*val[id.indexOf('pressure') >= 0 ? 0 : 2 ]/1000
        if (id.indexOf('pressure') >= 0) s-=0.243;
        else s*=val[2]*2
        $('#'+id.replace('size','area')).val(s)
    })
    $("input[name*='readings']").change(function(e){
        var id = $(this).attr('id')
        var s = $('#'+id.replace('readings','area')).val()
        var r = $(this).val()
        if (s*r) {
            var v = 0
            if (id.indexOf('pressure') >= 0) {
                //Сжатие
                v = (r/s).toFixed(2)
                if ($('#width').val() > 1)
                    v=(v * 1.2).toFixed(2)
            }
            else {
                //Изгиб
                v = (192.498*r*0.6/s).toFixed(2)
            }
            $('#'+id.replace('readings','value')).val(v)
        }
    })
})