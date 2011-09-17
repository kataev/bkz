dojo.provide("whs.CheckBox");

dojo.require('dijit.form.CheckBox');

dojo.declare("whs.CheckBox", dijit.form.CheckBox,{
    onChange:function(e){
        var table = dijit.byId('Brick');
        if (!table.fil){ table.fil={};table.query={};}
        if (!table.fil[this.name]){table.fil[this.name]={};}
        table.fil[this.name][this.value]=e;
        var query={};
        for (var name in table.fil) {
            var v = '';
            for (var value in table.fil[name]) {
                if (table.fil[name][value]){
                    if (value==9000){value='Брак'}
                    if (name=='weight'){if (value==1){value='Одинарный'};
                        if (value==1.4){value='Утолщенный'}}
                    v+=value+'|';
                    if (name=='total'){v='[^0] '}
                }
            }
            query[name]=new RegExp(v.slice(0,-1));
            v=undefined;
        }
        table.setQuery(query);
//        console.log(this,e,'change',table.fil);
    }
    
});