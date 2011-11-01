dojo.provide("whs.form.FKSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require("dojo.data.ItemFileWriteStore");

dojo.declare("whs.form.FKSelect", [dijit._Widget,dijit._Templated], {
    baseClass: 'FKSelect',name:'',
    templateString: dojo.cache('whs', 'template/FKSelect.html'),
    widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:[],
    render: function(item) {
//        console.log('render')
        var wid = this.id;
        var store = this.store;
        var id = whs.id_to_dict(store.getValues(item, 'id')).id;
        var name = whs.id_to_dict(store.getValues(item, 'id')).name;
        if (!this.value)this.value = {};
        if (this.value[name]) this.value[name].push(id); else this.value[name] = [id];
//        var tr = dojo.query('tr[name=' + name + ']' + '[id=' + id + ']', this.bodyNode)[0]
        tr = dojo.create('tr', {class:store.getValues(item, 'css'),'oper_id':id,name:name}, this.bodyNode);
        dojo.create('td', {innerHTML:store.getValues(item, 'brick')}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'amount')}, tr);
        if (store.getValues(item, 'price').length) {
            dojo.create('td', {innerHTML:store.getValues(item, 'price')}, tr);
            dojo.create('td', {innerHTML:store.getValues(item, 'price') * store.getValues(item, 'amount')}, tr);
        } else {dojo.create('td',{colspan:2},tr)}

        if (store.getValues(item, 'parent').length) {
            var i = store.getValues(item, 'parent')[0].id[0];
            var n = whs.id_to_dict(i).name; var d = whs.id_to_dict(i).id;
            var parent = dojo.query('[name=' + n + ']' + '[oper_id=' + d + ']',this.bodyNode)[0];
            if (parent) dojo.place(tr, parent, 'after');
        }
        if (!this[name + 'input']) this[name + 'input'] = dojo.create('select', {name:name, multiselect:'multiselect'
                                                                                    ,class:'hidden'}, this.domNode);
        dojo.create('option', {value:id,selected:'selected'}, this[name + 'input']);
            dojo.connect(menu,'onClose',function(){menu.uninitialize()})
            var menu = new dijit.Menu({targetNodeIds: [tr]});
            menu.addChild(new dijit.MenuItem({
                label:'Изменить операцию',
                onClick: function(event){
                    window.open('/' + name + '/' + id + '/#' + wid, '', "width=450,height=300,top=150,left=320");}
            }));
            menu.addChild(new dijit.MenuItem({
                label:'Посмотреть кирпич',
                onClick: function(event){
                    window.open('/brick/'+store.getValues(item,'brick_id')+'/');}
            }));
            menu.startup();
    },
    postCreate : function() {
        this.store = new dojo.data.ItemFileWriteStore({url:'store/'});
        var store = this.store;
        var id = this.id;
        var render = dojo.hitch(this, 'render');
        dojo.connect(store, 'onNew', function(item) { render(item); });
        store.fetch({query:{id:'*'},onItem:function(item) { render(item); }});
        var name = whs.names[window.location.pathname.split('/')[1]]
        for (var o in name) {
            dojo.create('a', {innerHTML:whs.upper(whs.locale[name[o]]),href:'/' + name[o] + '/'}, this.captionNode)
        }
        dojo.query('a', this.captionNode).connect('onclick', function(e) {
            dojo.stopEvent(e);
            window.open('/' + dojo.attr(this,'href').split('/')[1] + '/#' + id, '', "width=460,height=300,top=100,left=300");
        });
    },
    _getValueAttr:function() {
        return this.value;
    }
});