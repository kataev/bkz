dojo.provide('whs.operSelect');

//dojo.require('dojox.data.QueryReadStore');
//dojo.require('dojox.grid.DataGrid');
dojo.require('whs.oper');

dojo.declare('whs.operSelect', [dijit._Widget,dijit._Templated], {
    name:'',
    baseClass: 'operSelect',
    templateString: dojo.cache('whs', 'template/operSelect.html'),
    widgetsInTemplate:true,
    postCreate:function() {

    }
});