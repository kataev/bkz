dojo.provide("whs.br");

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');
dojo.require('dijit.Menu');


dojo.declare("whs.br", [dijit._Widget,dijit._Templated], {
    baseClass:'br',
    name:'No name',
    value:0,
    templateString:'<span class="${baseClass} ${class}">${name}</span>',
    _setnameAttr : function(val){
        this.name = val;
        this.domNode.innerHTML = val;

    },
    _getNameAttr : function(){
        return this.Name;
    },
    postCreate:function(){
//        this.inherited(arguments);
        this.domNode.innerHTML=this.title;
        var value = this.value
//        console.log(value);
    }
        });