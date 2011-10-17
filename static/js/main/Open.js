/*
 * User: bteam
 * Date: 17.10.11
 * Time: 10:29
 */
dojo.provide('whs.main.Open');

dojo.require('dojo.data.ItemFileReadStore');
dojo.require('dijit.Dialog');
dojo.require('dijit.form.NumberSpinner');
dojo.require('dijit.form.Button');
dojo.require('dijit.form.FilteringSelect');

dojo.addOnLoad(function(){
dijit.byId('OpenBill').onClick = function(e){
    var dialog = new dijit.Dialog({title:'Открыть накладную',style:'width:260px'});
    var node = dialog.containerNode;
    var year = dojo.create('span',null,node);
    dojo.create('span',{innerHTML:' номер:'},node);
    var number = dojo.create('span',null,node);
    var button = dojo.create('span',null,node);

    year = new dijit.form.NumberSpinner({style:'width:60px;',min:2000,name:'year',value:new Date().getFullYear()},year);
    number = new dijit.form.NumberSpinner({style:'width:60px;',min:0,name:'number',value:1},number);
    button = new dijit.form.Button({label:'открыть'},button);
    button.onClick = function(e){window.location = 'bill/'+year.get('value')+'/'+number.get('value')}

    dialog.show()
};

dijit.byId('OpenAgent').onClick = function(e){
    var dialog = new dijit.Dialog({title:'Открыть контрагента',style:'width:300px'});
    var node = dialog.containerNode;
    var select = dojo.create('span',null,node);
    var button = dojo.create('span',null,node);

    store = new dojo.data.ItemFileReadStore({url:'/agents/store/'});

    select = new dijit.form.FilteringSelect({style:'width:200px;',name:'agent',store:store,searchAttr:'label'},select);

    button = new dijit.form.Button({label:'открыть'},button);
    button.onClick = function(e){window.location = 'agent/'+whs.id_to_dict(select.get('value')).id}

    dialog.show()
};
    });