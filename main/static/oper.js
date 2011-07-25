dojo.provide('whs.oper');

//dojo.require('dijit.form.MultiSelect')
dojo.require('whs.brick')

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');

dojo.declare('whs.oper',[dijit._Widget, dijit._Templated],{
    baseClass: 'oper',
    selected:false,
    value:0,
    title:'',
    amount:0,
    info:'',
    name:'',
    brick_css:'',
    brick:'',
    brick_value:0,
    templateString: dojo.cache('whs', 'oper.html'),
    widgetsInTemplate:true,
    postCreate:function(){
        console.log(this.srcNodeRef,this);
    }

        });