dojo.provide("whs.brick");

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');

dojo.declare("whs.brick", [dijit._Widget, dijit._Templated], {
            baseClass: 'brick',
            name: 'No name',cl:'',mark:0,value: 0,total:'',view:'',weight:'','class':'',
            templateString: '<span class="${baseClass} ${class}"></span>',
            _setNameAttr: function(val) {
                this.name = this.srcNodeRef.innerHTML;
                this.domNode.innerHTML=this.name;
            },
            _getNameAttr: function() {
                return this.name;
            },
            _setTotalAttr: function(val) {
                var total_int = '';
                var s = val.split(',');
                var len = val.split(',').length;
                for (var i = 0; i < len; i++) {
                    total_int += s[i];
                }
                this.total = val;
                this.total_int = parseInt(total_int);
            },
            postCreate: function() {
//                console.log(this.name)
            }
        });


dojo.provide("whs.brick_tr");

dojo.declare('whs.brick_tr', whs.brick, {
            templateString: '<tr class="${baseClass} ${class}" ><td data-dojo-attach-point="nameNode"></td><td data-dojo-attach-point="totalNode"></td></tr>',
            _setNameAttr: function(val) {
                this.name = this.srcNodeRef.innerHTML;
                this.nameNode.innerHTML=this.name;
            },
            _setTotalAttr:function(val){
                this.totalNode.innerHTML = val;
            }

        });