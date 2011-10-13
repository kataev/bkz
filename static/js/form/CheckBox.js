dojo.provide("whs.form.CheckBox");

dojo.require('dijit.form.CheckBox');
dojo.require('dojo.hash');

dojo.declare("whs.form.CheckBox", dijit.form.CheckBox, {
    postCreate:function(e){
        this.table = dijit.byId('Brick');
        if (!this.table.fil) {
            this.table.fil = {};
            this.table.query = {};
        }
        if (!this.table.fil[this.name]) {this.table.fil[this.name] = {}}
    },
    onChange:function(e) {
        this.table.fil[this.name][this.value] = e;
        clearTimeout(whs.bricks.timeout);
        whs.bricks.timeout = setTimeout(whs.bricks.render,500);
    }

});