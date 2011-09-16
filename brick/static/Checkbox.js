dojo.provide("whs.Checkbox");

dojo.require('dijit.form.CheckBox');

dojo.declare("whs.Checkbox", dijit.form.CheckBox,{
    onChange:function(e){
        var table = dijit.byId('Brick');
        if (!table.fil){ table.fil={};table.query={};}
        if (!table.fil[this.name]){table.fil[this.name]={};}
        table.fil[this.name][this.value]=e;

        for (name in table.fil) {
            var v = '';
            for (val in table.fil[name]) {
                if (table.fil[name][val]) {
                    v+=val+'|'
                }
            }
//            console.log(v.slice(0,-1))
            table.query[name]=new RegExp(v.slice(0,-1))
        }
        table.render()
        console.log(this,e,'change',table.fil);
    }
    
})