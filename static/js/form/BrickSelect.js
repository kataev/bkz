dojo.provide("whs.form.BrickSelect");

dojo.require('dijit._Widget');
//dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require('dijit.Dialog');
dojo.require("dijit.layout.ContentPane");
dojo.require("dojo.data.ItemFileWriteStore");

dojo.provide('whs.form.Dialog');
dojo.declare('whs.form.Dialog', dijit.Dialog, {
    templateString: dojo.cache('whs', 'template/Dialog.html')
});

dojo.declare("whs.form.BrickSelect", [dijit._Widget,dijit._Templated], {
    name:'',
    baseClass: 'BrickSelect',
    templateString: dojo.cache('whs', 'template/BrickSelect.html'),
    widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:0,css:'',zero:true,
    constructor:function() { this.conteiner = new whs.form.Dialog(); },
    show:function(e) { this.conteiner.show(); },
    hide:function(e) { this.conteiner.hide(); },
    postMixInProperties:function(){
        if (this.srcNodeRef.nodeName =='SELECT') {
            var data = [];var value = 0;
            dojo.query('option',this.srcNodeRef).forEach(function(node){
                var item = {label:dojo.attr(node,'innerHTML'),id:'brick.brick__'+dojo.attr(node,'value'),
                total:dojo.attr(node,'total'),css:dojo.attr(node,'class')};
                data.push(item);
                if (dojo.attr(node,'selected')) value = dojo.attr(node,'value');
            });
            this.value = value;
            var store = this.store = new dojo.data.ItemFileWriteStore({data:{identifier:'id',label:'label',items:data}});
            dojo.empty(this.srcNodeRef);
        } else this.store = new dojo.data.ItemFileWriteStore({url:'/select/'});
    },
    postCreate:function() {
        var setLabel = dojo.hitch(this, '_setLabelAttr'); var zero = this.zero;
        var show = dojo.hitch(this, 'show'); var hide = dojo.hitch(this, 'hide');
        var setLabelClass = dojo.hitch(this, '_setLabelClassAttr');
        var setValue = dojo.hitch(this, '_setValueAttr'); var value = this.value;
        var content = this.conteiner;var store = this.store;
        dojo.connect(this.labelNode, 'onclick', function(e) { show(e) });
        var table = dojo.create('table', {id:'brick_select_table',class:this.baseClass,style:'width:300px;'}, content.containerNode);
        store.fetch({query:{id:'*'},onItem:function(item) {
//            if (!store.getValue(item, 'total') || zero) return;
            var id = whs.id_to_dict(store.getValues(item, 'id')).id;
            if (id == value) {
                setLabel(store.getLabel(item));
                setLabelClass(store.getValue(item, 'css'));
            }
            var tr = dojo.create('tr', {class:store.getValues(item, 'css'),id:id}, table);
            dojo.create('td', {innerHTML:store.getLabel(item)}, tr);
            dojo.create('td', {innerHTML:store.getValue(item, 'total')}, tr);
//            console.log(tr);
        }, onComplete: function (d) {
            dojo.query('tr', table).connect('onclick', function(e) {
                setValue(dojo.attr(this, 'id'));
                setLabelClass(dojo.attr(this, 'class'));
                setLabel(this.firstElementChild.innerHTML);
                hide()
            });
        }
        });
    },
    _setLabelAttr:function(val) {
        this.label = val;
        this.labelNode.innerHTML = val;
    },
    _setLabelClassAttr:function(val) {
        this.css = val;
        dojo.attr(this.labelNode, 'class', 'dijitTextBox BrickSelect ' + val);
    },
    _setValueAttr:function(val) {
        this.value = val;
        dojo.attr(this.inputNode, 'value', val);
    },_getValueAttr:function() {
        return {css:this.css,value:this.value,label:this.label}
    }
});

dojo.provide("whs.form.BrickSelect.StackConteiner");
dojo.declare('whs.form.BrickSelect.StackConteiner', whs.form.BrickSelect, {
    zero:false,
    constructor:function() {
        this.conteiner = new dijit.layout.ContentPane({region:'center',style:'padding:0px;'});
        var menu = new dijit.layout.BorderContainer({region:'left',class:'filter',style:'width:120px;'});
        var status = new dijit.layout.ContentPane({region:'bottom',
            content:'Шекните на строке с кирпичем для выбора',layoutPriority:1,style:'height:16px;padding:1px;'});
        this.filter_create(menu)
        var border = new dijit.layout.BorderContainer();
        border.addChild(status);
        border.addChild(this.conteiner)
        border.addChild(menu)
        dijit.byId('stack').addChild(border);

        dojo.subscribe('BrickSelect/Filter',function(str){status.domNode.innerHTML='#'+str.slice(1)});

    },
    show:function(e) { dijit.byId('stack').forward(); },
    hide:function(e) { dijit.byId('stack').back(); },
    filter_create:function(border){
        var menu1 = new dijit.layout.ContentPane({region:'top',style:'height:70px;padding:1px;'});
        border.addChild(menu1);

        var table = dojo.create('table',{class:'mark',value:'mark',style:'width:100%;height:100%;text-align:center'},menu1.domNode);
        var tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'100',value:100},tr);
        dojo.create('td',{innerHTML:'125',value:125},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'150',value:150},tr);
        dojo.create('td',{innerHTML:'175',value:175},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'200',value:200},tr);
        dojo.create('td',{innerHTML:'250',value:250},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Брак',value:9000},tr);
        dojo.create('td',{innerHTML:'Сброс'},tr);

        var menu2 = new dijit.layout.ContentPane({region:'top',style:'height:70px;padding:1px;'});
        border.addChild(menu2);

        table = dojo.create('table',{value:'class',style:'width:100%;height:100%;text-align:center'},menu2.domNode);
        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Красный',value:'red',class:'cl_red'},tr);
        dojo.create('td',{innerHTML:'Желтый',value:'ye',class:'cl_ye'},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Корич',value:'br',class:'cl_br'},tr);
        dojo.create('td',{innerHTML:'Светлый',value:'li',class:'cl_li'},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Белый',value:'wh',class:'cl_wh'},tr);
        dojo.create('td',{innerHTML:'Евро',value:'eu',class:'cl_eu'},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Прочие',value:'ot',class:'cl_ot'},tr);
        dojo.create('td',{innerHTML:'Сброс'},tr);

        var menu3 = new dijit.layout.ContentPane({region:'top',style:'height:40px;padding:1px;'});
        border.addChild(menu3);

        table = dojo.create('table',{class:'view',value:'view',style:'width:100%;height:100%;text-align:center'},menu3.domNode);
        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Лицевой',value:'facial',class:'facial'},tr);
        dojo.create('td',{innerHTML:'Рядовой',value:'common',class:'common'},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Сброс',colspan:2},tr);

        var menu4 = new dijit.layout.ContentPane({region:'top',style:'height:40px;padding:1px;'});
        border.addChild(menu4);

        table = dojo.create('table',{class:'weight',value:'weight',style:'width:100%;height:100%;text-align:center'},menu4.domNode);
        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Утолщен',value:'thickened',class:'thickened'},tr);
        dojo.create('td',{innerHTML:'Одинарн',value:'single',class:'single'},tr);

        tr = dojo.create('tr',{},table);
        dojo.create('td',{innerHTML:'Сброс',colspan:2},tr);

        var menu5 = new dijit.layout.ContentPane({region:'bottom',content:'&#8656;Назад',
            style:'height:16px;padding:1px;text-align:center;'});
        border.addChild(menu5);
        dojo.connect(menu5.domNode,'onclick',this.hide);


        dojo.query('td',border.domNode).connect('onclick',function(e){
            var table = this.parentElement.parentElement;
            var query = '';var filter = '';
            dojo.query('td',table).removeClass('active');
            if (dojo.attr(this,'value')) dojo.addClass(this,'active');
            var value = dojo.attr(this,'value');
            dojo.query('#brick_select_table tr').addClass('hide');
            dojo.query('td.active',border.domNode).forEach(function(node){
                var name = dojo.attr(node.parentElement.parentElement,'value');
                query+='.'+whs.prefix[name]+dojo.attr(node,'value');
                filter +='.'+node.innerHTML;
            });
            
            dojo.query('#brick_select_table tr'+query).removeClass('hide')

            dojo.publish('BrickSelect/Filter',[filter]);
        });

    }
});
