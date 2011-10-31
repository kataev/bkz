dojo.provide("whs.form.FKSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require("dojo.data.ItemFileWriteStore");

dojo.declare("whs.form.FKSelect", [dijit._Widget,dijit._Templated], {
    name:'',
    baseClass: 'FKSelect',
    templateString: dojo.cache('whs', 'template/FKSelect.html'),
    widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:[],
    render: function(item) {
        var store = this.store;var name = this.name;
        var id = store.getValues(item, 'id')
        this.value.push(id);
        var tr = dojo.create('tr', {class:store.getValues(item, 'css'),id:id}, this.bodyNode);
        dojo.create('td', {innerHTML:store.getValues(item, 'brick')}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'amount')}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'price')}, tr);
        dojo.create('td', {innerHTML:store.getValues(item, 'price') * store.getValues(item, 'amount')}, tr);
        dojo.create('option', {value:id,selected:'selected'}, this.inputNode);
        if (this.con) dojo.disconnect(this.con);
        this.con = dojo.query('tr',this.bodyNode).connect('onclick',function(e){
            window.open(whs.id_to_url(dojo.attr(this,'id')),'asd',"width=450,height=300,top=100,left=300");
        })
    },
    postCreate : function() {
        this.store = new dojo.data.ItemFileWriteStore({url:this.name + '/'});
        var store = this.store;
        var input = this.inputNode;
        var body = this.bodyNode;
        var value = this.value;
        var render = dojo.hitch(this,'render');
        dojo.connect(store,'onNew',function(item){render(item);})
        store.fetch({query:{id:'*'},onItem:function(item) {
            render(item);
        }, onComplete: function (d) { }
        });

        var name = this.name;
        window[this.baseClass + name] = this;
        dojo.connect(this.captionNode, 'onclick', function(e) {

            window.open('/' + name + '/','asd',"width=450,height=300,top=100,left=300");
        });
    }
    ,
    _getValueAttr:function() {
        return this.value;
    }
})
    ;