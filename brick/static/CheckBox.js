dojo.provide("whs.CheckBox");

dojo.require('dijit.form.CheckBox');

dojo.declare("whs.CheckBox", dijit.form.CheckBox,{
    onChange:function(e){
        var table = dijit.byId('Brick');
        if (!table.fil){ table.fil={};table.query={};}
        if (!table.fil[this.name]){table.fil[this.name]={};}
        table.fil[this.name][this.value]=e;
        var query={};
        for (name in table.fil) {
            var v = '';
            for (val in table.fil[name]) {
                if (table.fil[name][val]){
                    if (val==9000){val='Брак'}
                    if (name=='weight'){if (val==1){val='Одинарный'};if (val==1.4){val='Утолщенный'}}
                    v+=val+'|'
                    if (name=='total'){v='[^0] '}
                }
            }
            query[name]=new RegExp(v.slice(0,-1));
            v=undefined;
        }
        table.setQuery(query);
//        console.log(this,e,'change',table.fil);
    }
    
})