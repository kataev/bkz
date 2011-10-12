dojo.provide("whs.form.CheckBox");

dojo.require('dijit.form.CheckBox');

dojo.declare("whs.form.CheckBox", dijit.form.CheckBox, {
    onChange:function(e, dojo) {
        var table = dijit.byId('Brick');
        if (!table.fil) {
            table.fil = {};
            table.query = {};
        }
        if (!table.fil[this.name]) {table.fil[this.name] = {}}
        table.fil[this.name][this.value] = e;
        var query = {}; var css = '';
        order = ['weight','mark','brick_class','view'];
        for (var i in order) {
            var name = order[i];
            if (name in table.fil){
            var v = '';
            for (var value in table.fil[name]) {if (table.fil[name][value]) v+=value+'|';}
            if (v) css+='('+v.slice(0,-1)+').*';
            query.css = new RegExp(css);
            v = undefined;
        }}
        table.setQuery(query);
        var tableTotal = dijit.byId('BricksTotal');
        var scroller = table.scroller;
        if (scroller.windowHeight >= scroller.averageRowHeight * scroller.rowCount)
            BrickLayout[0].width = '265px';
        else BrickLayout[0].width = '280px';
        tableTotal.render();
    }

});