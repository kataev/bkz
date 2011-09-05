dojo.provide("whs.brick");

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');

dojo.declare("whs.brick", [dijit._Widget, dijit._Templated], {
            baseClass: 'brick',selected:false,total:'',sold:'',tr_p:'',tr_m:'',n_m:'',
            name: 'No name',cl:'',mark:0,value: 0,view:'',weight:'','class':'',//TODO: clear mark and other, do css class filter
            templateString: '<span class="${baseClass} ${class}"></span>',
            _setNameAttr: function(val) {
                this.name = this.srcNodeRef.innerHTML;
                this.domNode.innerHTML = this.name;
            },
            _getNameAttr: function() {
                return this.name;
            },
            _getSelectedAtrr:function(value) {
                console.log(value);
            },
            postCreate: function() {
//                console.log(this.name)
            }
        });


dojo.provide("whs.brick_tr");

dojo.declare('whs.brick_tr', whs.brick, {
            templateString: '<tr value="${value}" class="${baseClass} ${class}" ><td class="nameNode" data-dojo-attach-point="nameNode"></td><td data-dojo-attach-point="totalNode"></td></tr>',
            _setNameAttr: function(val) {
                this.name = this.srcNodeRef.innerHTML;
                this.nameNode.innerHTML = this.name;
            },
            _setTotalAttr:function(val) {
                this.totalNode.innerHTML = val;
            },
            _setSelectedAttr:function(val) {
                if (val) {
                    dojo.attr(this.domNode, 'selected', 'selected');
                    console.log('selected', this.value)
                }
                else {
                    if (this.selected) {
                        dojo.removeAttr(this.domNode, 'selected', 'selected');
                        console.log('remove selected', this.value);
                    }
                }
                dojo.toggleClass(this.domNode,'selected');
            },
            postCreate:function() {
                var input = this.input;
                var select = dojo.hitch(this, '_setSelectedAttr');
                var domNode = this.domNode;
                dojo.connect(domNode, 'onclick', function(e) {
                    dojo.query('[selected]', domNode.parentNode).forEach(function(node) {
//                        console.log(node,'remove sel');
                        dojo.removeAttr(node, 'selected');
                        dojo.removeClass(node, 'selected');
                    });
                    select(true);

                })
            }

        });