dojo.provide("whs.OpersWidget");

dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
//dojo.require("dijit.layout.ContentPane");

dojo.declare("whs.OpersWidget", [dijit._Widget, dijit._Templated], {
            label:'Loading...',
            region:'bottom',
            templateString:
                    dojo.cache("whs.OpersWidget", "templates/OpersWidget.html"),
            baseClass: "OpersWidget",

            postCreate: function() {
//                var domNode = this.domNode;
                this.inherited(arguments);

//                dijit.byNode(this.Border).resize();
            }
        });
