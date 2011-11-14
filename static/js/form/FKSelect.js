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
    render: function(item) { //Функция отображения строки с операциями.
        var pop = this.popup;var style='';
        var wid = this.id; var store = this.store;
        var id = whs.id_to_dict(store.getValues(item, 'id')).id;
        var name = whs.id_to_dict(store.getValues(item, 'id')).name;
        var parent = store.getValue(item,'parent');
        if (!this.value)this.value = {};
        if (this.value[name]) this.value[name].push(id); else this.value[name] = [id];
        var tr = dojo.create('tr', {class:store.getValues(item, 'css'),'oper_id':id,name:name,title:store.getValues(item, 'label')+store.getValues(item, 'info')}, this.bodyNode);
        if (parent) {this.parents.push([tr,store.getValue(parent,'id')]);dojo.addClass(tr,'parent')}
        dojo.create('td', {innerHTML:store.getValues(item, 'brick'),style:style}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'amount'),class:'amount l'}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'tara'),class:'tara'}, tr);
        if (store.getValues(item, 'price').length) {
            dojo.create('td', {class:'price',innerHTML:store.getValues(item, 'price')}, tr);
            dojo.create('td', {class:'sum',innerHTML:store.getValues(item, 'price') * store.getValues(item, 'amount')}, tr);
        } else { dojo.create('td', {colspan:2}, tr) }

        if (store.getValues(item, 'parent').length) { //
            var i = whs.id_to_dict(store.getValues(item, 'parent')[0].id[0]);
            var parent = dojo.query('[name=' + i.name + ']' + '[oper_id=' + i.id + ']', this.bodyNode)[0];
            if (parent) dojo.place(tr, parent, 'after');
        }
        if (!this[name + 'input']) this[name + 'input'] = dojo.create('select', {name:name, multiselect:'multiselect'
            ,class:'hidden'}, this.domNode);
        dojo.create('option', {value:id,selected:'selected'}, this[name + 'input']);
        dojo.connect(menu, 'onClose', function() { menu.uninitialize() })
        var menu = new dijit.Menu({targetNodeIds: [tr]});
        menu.addChild(new dijit.MenuItem({ label:'Изменить операцию',
            onClick: function(event) { window.open('/' + name + '/' + id + '/','', pop); }
        }));
        menu.addChild(new dijit.MenuItem({ label:'Посмотреть кирпич',
            onClick: function(event) { window.open('/brick/' + store.getValues(item, 'brick_id') + '/'); }
        }));
        menu.startup();
    },
    refresh:function(){
        var render = dojo.hitch(this, 'render');var parents = this.parents = [];
        var tbody = this.bodyNode;var tfoot = this.footNode;        
        dojo.empty(tbody); dojo.empty(tfoot);
        dojo.query('select',this.domNode).empty()
        this.store.fetch({query:{id:'*'},
            onItem:function(item) { render(item); },
            onError:function(e){return},
            onComplete:function(e){
                dojo.forEach(parents,function(n){
                    var id = whs.id_to_dict(n[1])
                    var node = dojo.query('[oper_id='+id.id+'][name='+id.name+']',tbody)[0];
                    if (node) dojo.place(n[0],node,'after');
                });
                var names = {}; dojo.query('tr',tbody).attr('name').forEach(function(e){names[e]=true;});
                for (var name in names){
                    var tr = dojo.create('tr',null,tfoot);
                    dojo.create('th',{innerHTML:whs.upper(whs.locale_plural[name]),style:'text-align:right;padding-right:5px;'},tr);
                    var opers = dojo.query('[name='+name+']',tbody);
                    dojo.create('th',{class:'amount d',innerHTML:opers.query('td.amount').attr('innerHTML').reduce(function(e,w){return parseInt(e)+parseInt(w);})},tr);
                    dojo.create('th',{class:'tara',innerHTML:opers.query('td.tara').attr('innerHTML').reduce(function(e,w){return parseInt(e)+parseInt(w);})},tr);
                    dojo.create('th',null,tr);
                    if (opers.query('td.price').length)
                        dojo.create('th',{class:'tara',innerHTML:opers.query('td.sum').attr('innerHTML').reduce(function(e,w){return parseInt(e)+parseInt(w);})},tr);
                    else dojo.create('th',null,tr);
                }
            }
        });
    },
    postCreate : function() {
        var store = this.store = new dojo.data.ItemFileWriteStore({url:'store/'});
        var pop = this.popup;
        var id = this.id; var body = this.bodyNode;
        var render = dojo.hitch(this, 'render'); var refresh = dojo.hitch(this, 'refresh');
        this.refresh();
        dojo.connect(this.store,'onNew',function(e){});
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
                onItem:function(item_old) { count++; for (var f in item){ store.setValue(item_old,f,item[f]); } },
                onComplete:function(complite) {
                    if (!count) { item.id = data.id; store.newItem(item); }
                    refresh();
                }
            });
        });
    },
    _getValueAttr:function() {
        return this.value;
    }
});