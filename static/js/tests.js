function get_area_and_volume(id,size) {
    var val = $.map(size.split('x'),function(v){return parseFloat(v)})
    var s = val[1]*val[id.indexOf('pressure') >= 0 ? 0 : 2 ]/1000
    if (id.indexOf('pressure') >= 0) 
        s-=0.243;
    else 
        s*=val[2]*2
    return [s,val[0] * val[1] * val[2] / Math.pow(100*10,3)]
}


$(function(){
    $("input[name*='size']").mask('999.9 x 999.9 x 99.9').change(function(e){
        var id = $(this).attr('id')
        var size = $(this).val()
        var q = get_area_and_volume(id,size)
        $('#'+id.replace('size','area')).val(q[0]).attr('title','Объем м³: '+q[1])
        $('#'+id.replace('size','readings')).change()
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

    $('#form').on('change',"input[name='volume'],input[name='weight']",function(e){
        var id = $(e.delegateTarget).find('input[name="volume"]:checked').val()
        var size = $('#id_'+id+'-size').val()
        var w = $('#id_weight').val()
        if (size && w) {
            var vol = get_area_and_volume(id,size)[1]
            var dens = (w/vol).toFixed(2)
            $('#id_density').val(dens)
            var cad = ''
            if (dens <= 800) cad = 0.8;
            if (dens >= 801 && dens <= 1000) cad = 1.0;
            if (dens >= 1001 && dens <= 1200) cad = 1.2;
            if (dens >= 1201 && dens <= 1400) cad = 1.4;
            if (dens >= 1400) cad = 2.0;
            $('#id_cad').val(cad)
        }
    })
})