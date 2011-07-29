dojo.provide('whs.operContainer');

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');
dojo.require("dijit.Dialog");

dojo.declare('whs.operContainer', [dijit._Widget, dijit._Templated], {
            opers:{},
            query:[],
            baseClass: 'operContainer',
            templateString: dojo.cache('whs', 'template/operContainer.html'),
            widgetsInTemplate:true
        });