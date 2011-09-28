dependencies = {
    layers: [
        {
            name: "../whs/form.js",
            resourceName: "whs.form",
            dependencies: [
                "whs.Form",
            ]
        },
        {
            name: "../whs/core.js",
            resourceName: "whs.core",
            dependencies: [
                "whs.script"
            ]
        }
    ],
    prefixes: [
        ["dijit", "../dijit"],
        ["dojox", "../dojox"],
        ["whs", "/home/bteam/static"]
    ]
}

