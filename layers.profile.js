dependencies = {
    layers: [
        {
            name: "../whs/form/Form.js",
            resourceName: "whs.form.Form",
            dependencies: [
                "whs.form.Form",
            ]
        },
        {
            name: "../whs/form/Sold.js",
            resourceName: "whs.form.Sold",
            dependencies: [
                "whs.form.Sold",
            ]
        },
        {
            name: "../whs/core.js",
            resourceName: "whs.core",
            dependencies: [
                "whs.core"
            ]
        }//TODO: отрабоать тут!
    ],
    prefixes: [
        ["dijit", "../dijit"],
        ["dojox", "../dojox"],
        ["whs", "/home/bteam/whs/bill/static/js"]
    ]
}

