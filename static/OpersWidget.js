dojo.provide("whs.OpersWidget");

dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
//dojo.require("dijit.layout.BorderContainer");
//dojo.require("dijit.layout.ContentPane");
//dojo.require("dijit.MenuBar");
//dojo.require("dijit.MenuBarItem");


dojo.declare("whs.OpersWidget", [dijit._Widget, dijit._Templated], {
            constructor: function(name,id){
                                
            },

            label:'Loading...',

//            templateString:
//                    dojo.cache("whs.OpersWidget", "templates/OpersWidget.html"),
            baseClass: "OpersWidget",
            resize: function(){},
            postCreate: function() {
//                dojo.parser.parse(this.domNode);
                tableNode=this.tableNode
                this.inherited(arguments);
                dojo.xhrGet({url:'./form/solds/',handleAs:'json'}).then(function(data){
                    var tr = dojo.create('tr',{innerHTML:data.html},tableNode);
                    dojo.parser.parse(tableNode);
                })
//                dijit.byNode(this.Border).resize();
            }
        });
