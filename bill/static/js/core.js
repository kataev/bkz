dojo.provide('whs.core');

dojo.registerModulePath("whs", "/static/js");

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");

dojo.require("dijit.MenuBar");
dojo.require("dijit.MenuItem");
dojo.require("dijit.PopupMenuBarItem");

var dojoConfig = {
            isDebug: true,
            locale: 'Ru-ru'
            ,'parseOnLoad':true
        };

dojo.addOnLoad(function(){
    dojo.query('.bills_table tr').connect('onclick',function(evt){
        window.location = '/bill/' + dojo.attr(this,'pk') + '/';
    });
});

dojo.provide('whs.id_to_url');

whs.id_to_url = function(s) {
    s = ''+s;
    var name = s.split('.')[1].split('__')[0];
    var id = s.split('.')[1].split('__')[1];
    return '/'+name+'/'+id+'/';
};

dojo.provide('whs.id_to_dict');
whs.id_to_dict = function(s) {
    s = ''+s;
    var name = s.split('.')[1].split('__')[0];
    var id = s.split('.')[1].split('__')[1];
    return {name:name,id:id};
};
