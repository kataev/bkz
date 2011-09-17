dojo.registerModulePath("whs", "/static");

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");

dojo.require("dijit.MenuBar");
dojo.require("dijit.MenuItem");
dojo.require("dijit.PopupMenuBarItem");

var dojoConfig = {
            isDebug: true,
            locale: 'Ru-ru'
//            'parseOnLoad':true
        };

dojo.addOnLoad(function(){
    dojo.query('.bills_table tr').connect('onclick',function(evt){
        window.location = '/bill/' + dojo.attr(this,'pk') + '/';
    });
});