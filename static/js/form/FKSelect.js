dojo.provide("whs.form.FKSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require("dojo.data.ItemFileWriteStore");

dojo.declare("whs.form.FKSelect", [dijit._Widget,dijit._Templated], {
    baseClass: 'FKSelect',name:'',
    templateString: dojo.cache('whs', 'template/FKSelect.html'),
    widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:[],parents:[],
    popup:'width=500,height=300,top=100,left=350',
    render: function(item) {
        var pop = this.popup;var style='';
        var wid = this.id; var store = this.store;
        var id = whs.id_to_dict(store.getValues(item, 'id')).id;
        var name = whs.id_to_dict(store.getValues(item, 'id')).name;
        var parent = store.getValue(item,'parent');
        if (!this.value)this.value = {};
        if (this.value[name]) this.value[name].push(id); else this.value[name] = [id];
        var tr = dojo.create('tr', {class:store.getValues(item, 'css'),'oper_id':id,name:name,title:store.getValues(item, 'label')+store.getValues(item, 'info')}, this.bodyNode);
        if (parent) this.parents.push([tr,store.getValue(parent,'id')]);
        if (name=='sold') style='padding-left:20px;';
        dojo.create('td', {innerHTML:store.getValues(item, 'brick'),style:style}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'amount')}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'tara')}, tr);
        if (store.getValues(item, 'price').length) {
            dojo.create('td', {innerHTML:store.getValues(item, 'price')}, tr);
            dojo.create('td', {innerHTML:store.getValues(item, 'price') * store.getValues(item, 'amount')}, tr);
        } else {
            dojo.create('td', {colspan:2}, tr)
        }

        if (store.getValues(item, 'parent').length) {
            var i = store.getValues(item, 'parent')[0].id[0];
            var n = whs.id_to_dict(i).name;
            var d = whs.id_to_dict(i).id;
            var parent = dojo.query('[name=' + n + ']' + '[oper_id=' + d + ']', this.bodyNode)[0];
            if (parent) dojo.place(tr, parent, 'after');
        }
        if (!this[name + 'input']) this[name + 'input'] = dojo.create('select', {name:name, multiselect:'multiselect'
            ,class:'hidden'}, this.domNode);
        dojo.create('option', {value:id,selected:'selected'}, this[name + 'input']);
        dojo.connect(menu, 'onClose', function() {
            menu.uninitialize()
        })
        var menu = new dijit.Menu({targetNodeIds: [tr]});
        menu.addChild(new dijit.MenuItem({
            label:'Изменить операцию',
            onClick: function(event) {
                window.open('/' + name + '/' + id + '/','', pop);
            }
        }));
        menu.addChild(new dijit.MenuItem({
            label:'Посмотреть кирпич',
            onClick: function(event) {
                window.open('/brick/' + store.getValues(item, 'brick_id') + '/');
            }
        }));
        menu.startup();
    },
    refresh:function(){
        var render = dojo.hitch(this, 'render');var body = this.bodyNode;
        dojo.empty(body); var parents = this.parents;
        this.store.fetch({query:{id:'*'},
            onItem:function(item) { render(item); },
            onError:function(e){return},
            onComplete:function(e){
                dojo.forEach(parents,function(n){
                    var id = whs.id_to_dict(n[1])
                    var node = dojo.query('[oper_id='+id.id+'][name='+id.name+']',body)[0];
                    if (node) dojo.place(n[0],node,'after');
                });
            }
        });
    },
    postCreate : function() {
        var pop = this.popup;
        this.store = new dojo.data.ItemFileWriteStore({url:'store/'});
        var store = this.store;
        var id = this.id; var body = this.bodyNode;
        var render = dojo.hitch(this, 'render');
        var refresh = dojo.hitch(this, 'refresh');
//        dojo.connect(store, 'onNew', function(item) {
//            render(item);
//        });
        this.refresh();
        var name = whs.names[window.location.pathname.split('/')[1]]
        for (var o in name) {
            dojo.create('a', {innerHTML:whs.upper(whs.locale[name[o]]),href:'/' + name[o] + '/'}, this.captionNode)
        }
        dojo.query('a', this.captionNode).connect('onclick', function(e) {
            dojo.stopEvent(e);
            window.open('/' + dojo.attr(this, 'href').split('/')[1] + '/', '',pop);
        });
        dojo.subscribe("whs/FKSelect", function(data) {
            var count = 0;
            var item = data.value; var brick = item.brick; item.brick = brick.label;
            item.brick_id = brick.value; item.css = brick.css;
            store.fetch({query:{id:data.id},
                onItem:function(item_old) {
                    count++;
                    console.log(item, 'found!');
                    for (var f in item){
//                        console.log(f,item[f])
                        store.setValue(item_old,f,item[f]);
                    }
                },
                onComplete:function(complite) {
                    if (!count) {
                        console.log(data, 'тю тю');
                        item.id = data.id;
                        store.newItem(item);
                    }
                    refresh();
                }
            });

        });
    },
    _getValueAttr:function() {
        return this.value;
    }
});