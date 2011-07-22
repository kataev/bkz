dojo.provide("whs.select");


//dojo.require('dijit.form._FormWidget');
dojo.require('dijit._Widget');
dojo.require('whs.brick');
dojo.require('dijit._Templated');
//dojo.require("dojo.store.Memory");
//dojo.require("dijit.Dialog");

dojo.declare("whs.select", [dijit._Widget,dijit._Templated], {
            name:'',
            baseClass: 'selectBrick',
            templateString: '<table name="${name}" data-dojo-attach-point="containerNode"></table>',
            widgetsInTemplate:true,
            label:'Щелкните для выбора кирпича'
        });