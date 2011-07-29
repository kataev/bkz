dojo.provide('whs.oper');

//dojo.require('dijit.form.MultiSelect')
dojo.require('whs.brick')

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');
dojo.require('dijit.Dialog')

dojo.declare('whs.oper',[dijit._Widget, dijit._Templated],{
    baseClass: 'oper',
    selected:false,
    value:0,
    title:'',
    amount:0,
    tara:0,
    info:'',
    name:'',
    brick_css:'',
    brick:'',
    brick_value:0,
    templateString: dojo.cache('whs', 'template/oper.html'),
    widgetsInTemplate:true,
    _setInfoAttr: function(val) {
                this.info = this.srcNodeRef.innerHTML;
            },
    postCreate:function(){

//        console.log(this.info);
        var dialog=null;
        var oper = this.oper;
        var value = this.value;
        dialog = new dijit.Dialog({href:'/form/'+oper+'/'+value+'/',title:'Просмотр и редактирование операции'});
        dojo.connect(this.domNode,'onclick',function(){
            if (oper){
                dialog.show()
            }
        });
    }
        });


dojo.provide('whs.oper_tr');

dojo.declare('whs.oper_tr',whs.oper,{
    templateString: dojo.cache('whs', 'template/oper_tr.html')
        });