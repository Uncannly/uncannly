requirejs.config({ 
    baseUrl: 'static/js',
    paths: { 
        'jquery': '../vendor/jquery-3.1.1.min',
        'Clipboard': '../vendor/clipboard.min',
    }
});

requirejs([
    "requestWords",
    "bothModes",
    "controls",
    "helpers",
    "randomMode", 
    "topMode",
    "responsive",
    "jquery",
    "Clipboard",
]);