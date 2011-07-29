dojo.provide('whs.operSelect');

dojo.require('whs.oper')
dojo.require('whs.operContainer')

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');

dojo.declare('whs.operSelect',[dijit._Widget, dijit._Templated],{
    name:'',
    value:[],
    baseClass: 'operSelect',
    templateString: dojo.cache('whs', 'template/operSelect.html'),
    widgetsInTemplate:true,
    _getValueAttr:function(){
        var value = [];
        if (this.inputNode){
            dojo.query('tr',this.inputNode).forEach(function(node){
                value.push(dojo.attr(node,'value'));
            });
        }
        return value;
    },
    postCreate:function(){
        var form = dijit.getEnclosingWidget(this.domNode.parentNode);
        if (!form.operContainer){
            var node = this.domNode.parentNode.parentNode;
            form.operContainer= new whs.operContainer({node:node});
        }
        form.operContainer.add(this);
    }

        });