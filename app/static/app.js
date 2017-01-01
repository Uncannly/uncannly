requirejs.config({ 
	baseUrl: 'static/js',
  paths: { 
    'jquery': '../vendor/jquery-3.1.1.min',
    'Clipboard': '../vendor/clipboard.min',
    'filesaver': '../vendor/FileSaver.min'
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
	"audio",
	"jquery",
	"Clipboard",
	"filesaver"
]);