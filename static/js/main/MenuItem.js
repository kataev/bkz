/*
 * User: bteam
 * Date: 11.10.11
 * Time: 15:27
 */
dojo.provide("whs.main.MenuItem");

dojo.declare("whs.main.MenuItem", dijit.MenuItem, {
    _onClick: function(e) {
        this.getParent().onItemClick(this, e);
    }
})