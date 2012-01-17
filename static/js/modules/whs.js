// Use an IIFE...
// (http://benalman.com/news/2010/11/immediately-invoked-function-expression/)
// to assign your module reference to a local variable, in this case Example.
//
// Change line 16 'Example' to the name of your module, and change line 38 to
// the lowercase version of your module name.  Then change the namespace
// for all the Models/Collections/Views/Routers to use your module name.
//
// For example: Renaming this to use the module name: Project
//
// Line 16: (function(Project) {
// Line 38: })(namespace.module("project"));
//
// Line 18: Project.Model = Backbone.Model.extend({
//
(function (whs) {

    whs.Model = Backbone.Model.extend({ /* ... */ });
    whs.Collection = Backbone.Collection.extend({ /* ... */ });
    whs.Router = Backbone.Router.extend({
        routes:{
            "brick":"brick"
        },
        brick:function(){
            console.log('brick')
        }
    });

    // This will fetch the tutorial template and render it.
    whs.Views.Tutorial = Backbone.View.extend({
        template:"/static/js/templates/example.html",

        render:function (done) {
            var view = this;

            // Fetch the template, render it to the View element and call done.
            namespace.fetchTemplate(this.template, function (tmpl) {
                view.el.innerHTML = tmpl();

                done(view.el);
            });
        }
    });

})(namespace.module("whs"));
