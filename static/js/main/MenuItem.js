/*
 * User: bteam
 * Date: 11.10.11
 * Time: 15:27
 */
dojo.provide("whs.main.MenuBarItem");
dojo.require('dijit.MenuBarItem');
dojo.declare("whs.main.MenuBarItem", dijit.MenuBarItem, {
    _onClick: function(e) {
        this.getParent().onItemClick(this, e);
    }
});

dojo.provide("whs.main.MenuItem");
dojo.require('dijit.MenuItem');
dojo.declare("whs.main.MenuItem", dijit.MenuItem, {
    _onClick: function(e) {
        this.getParent().onItemClick(this, e);
    }
})