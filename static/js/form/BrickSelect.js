dojo.provide("whs.form.BrickSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require('dijit.Dialog');
dojo.require("dijit.layout.ContentPane");
dojo.require("dojo.data.ItemFileReadStore");

dojo.provide('whs.form.Dialog');
dojo.declare('whs.form.Dialog',dijit.Dialog,{
    templateString: dojo.cache('whs', 'template/Dialog.html')
        });

dojo.declare("whs.form.BrickSelect", [dijit._Widget,dijit._Templated], {
            name:'',
            baseClass: 'BrickSelect',
            templateString: dojo.cache('whs', 'template/BrickSelect.html'),
            widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:0,css:'',
    constructor:function(){console.log('construct');this.conteiner = new whs.form.Dialog();},
    show:function(e){this.conteiner.show();},
    hide:function(e){this.conteiner.hide();},
            postCreate:function() {
                var setLabel = dojo.hitch(this, '_setLabelAttr');
                var show = dojo.hitch(this, 'show');
                var hide = dojo.hitch(this, 'hide');
                var setLabelClass = dojo.hitch(this, '_setLabelClassAttr');
                var setValue = dojo.hitch(this, '_setValueAttr');
                var value = this.value;
                var content = this.conteiner;
                dojo.connect(this.labelNode, 'onclick', function(e) { show(e) });
                this.store = new dojo.data.ItemFileReadStore({url:'/select/'});
                var store = this.store;
                var table = dojo.create('table',{class:this.baseClass},content.containerNode);
                store.fetch({query:{id:'*'},onItem:function(item){
                    var id = whs.id_to_dict(store.getValues(item,'id')).id;
                    if (id == value){
                        setLabel(store.getLabel(item));
                        setLabelClass(store.getValue(item,'css'));
                    }
                    var tr = dojo.create('tr',{class:store.getValues(item,'css'),id:id},table);
                    dojo.create('td',{innerHTML:store.getLabel(item)},tr);
                    dojo.create('td',{innerHTML:store.getValue(item,'total')},tr);
                    }, onComplete: function (d){
                    dojo.query('tr',table).connect('onclick',function(e){
                        setValue(dojo.attr(this,'id'));
                        setLabelClass(dojo.attr(this,'class'));
                        setLabel(this.firstElementChild.innerHTML);
                        hide()
                    });
                }
                });
            },
            _setLabelAttr:function(val) {
                this.label = val;
                this.labelNode.innerHTML=val;
            },
            _setLabelClassAttr:function(val) {
                this.css = val;
                dojo.attr(this.labelNode,'class','dijitTextBox BrickSelect '+val);
            },
            _setValueAttr:function(val) {
                this.value = val;
                dojo.attr(this.inputNode,'value',val);
            },_getValueAttr:function(){
        return {css:this.css,value:this.value,label:this.label}
    }
        });

dojo.provide("whs.form.BrickSelect.StackConteiner");
dojo.declare('whs.form.BrickSelect.StackConteiner',whs.form.BrickSelect,{
    constructor:function(){
        console.log('constuct stack');
        this.conteiner = new dijit.layout.ContentPane();
//        var border = new dijit.layout.BorderContainer({region:'center'});
//        border.addChild(this.conteiner);


        dijit.byId('stack').addChild(this.conteiner);
    },
    show:function(e){ dijit.byId('stack').forward(); },
    hide:function(e){ dijit.byId('stack').back(); }
});
