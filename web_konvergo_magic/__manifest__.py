{
    "name": "Konvergo MAGIC",
    "summary": "Konvergo MAGIC baseline for integration with Konvergo ERP",
    "version": "14.0.1.0.0",
    "author": "Konvergo",
    "maintainer": "Konvergo",
    "website": "https://konvergo.com",
    "license": "LGPL-3",
    "application": True,
    "category": "Website",
    "depends": [
        "base",
        "web",
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
    ],
    "installable": True,
}