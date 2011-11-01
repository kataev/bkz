dojo.provide("whs.form.FKSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require("dojo.data.ItemFileWriteStore");

dojo.declare("whs.form.FKSelect", [dijit._Widget,dijit._Templated], {
    baseClass: 'FKSelect',
    templateString: dojo.cache('whs', 'template/FKSelect.html'),
    widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:{}//,
//    render: function(item) {
//        var store = this.store;
//        var id = whs.id_to_dict(store.getValues(item, 'id')).id
//        var name = whs.id_to_dict(store.getValues(item, 'id')).name
//        if (this.value[name]) this.value[name].push(id);else this.value[name] = [id];
//        var tr = dojo.create('tr', {class:store.getValues(item, 'css'),id:id,name:name}, this.bodyNode);
//        dojo.create('td', {innerHTML:store.getValues(item, 'brick')}, tr);
//        dojo.create('td', {innerHTML:store.getValues(item, 'amount')}, tr);
////        if (store.getValues(item, 'price')) {
////            dojo.create('td', {innerHTML:store.getValues(item, 'price')}, tr);
////            dojo.create('td', {innerHTML:store.getValues(item, 'price') * store.getValues(item, 'amount')}, tr);
////        }
////        if (store.getValues(item, 'parent')){
////            var parent = dojo.query([])
////        }
////        this[name+'input'] = dojo.create('select',{name:name,multiselect:'multiselect'},this.domNode);
////        dojo.create('option', {value:id,selected:'selected'}, this[name+'input']);
////        if (this.con) dojo.disconnect(this.con);
////        this.con = dojo.query('tr', this.bodyNode).connect('onclick', function(e) {
////            window.open(whs.id_to_url(dojo.attr(this, 'id')), 'asd', "width=450,height=300,top=100,left=300");
////        });
//    },
//    postCreate : function() {
//        this.store = new dojo.data.ItemFileWriteStore({url:this.name + '/'});
//        var store = this.store;
////        var render = dojo.hitch(this, 'render');
////        dojo.connect(store, 'onNew', function(item) { render(item); });
////        store.fetch({query:{id:'*'},onItem:function(item) { render(item); } });
//
////        var name = this.name;
////        window[this.baseClass + name] = this;
////        dojo.connect(this.captionNode, 'onclick', function(e) {
////            window.open('/' + name + '/', 'asd', "width=450,height=300,top=100,left=300");
////        });
//    },
//    _getValueAttr:function() {
//        return this.value;
//    }
});