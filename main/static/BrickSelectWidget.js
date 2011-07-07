dojo.provide("whs.BrickSelectWidget");


dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
dojo.require("whs.BrickWidget");

dojo.declare("whs.BrickSelectWidget", whs.BrickWidget, {
                baseClass:'',
                templateString:
                    dojo.cache("whs.BrickSelectWidget", "templates/BrickSelectWidget.html")

        });
