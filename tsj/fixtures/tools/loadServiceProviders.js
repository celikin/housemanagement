// http://shakhty.caddress.ru/category/kommunalnye-uslugi/page/95
function loadScript(url, callback)
{
	var head = document.getElementsByTagName("head")[0];
	var script = document.createElement("script");
	script.src = url;
	var done = false;
	script.onload = script.onreadystatechange = function()
	{
		if( !done && ( !this.readyState 
					|| this.readyState == "loaded" 
					|| this.readyState == "complete") )
		{
			done = true;
			callback();
		}
	};
	head.appendChild(script);
};

loadScript("http://code.jquery.com/jquery-2.1.1.min.js", function(){
	var siteUri = "http://shakhty.caddress.ru/category/kommunalnye-uslugi/page/";
	var doc = $('body').empty();
	for(var i = 1; i <= 166; i++){
		$.get(siteUri+i, '', function(data){
			$('<div/>').html(data).find('.record').filter(':contains(ВЛАДИВОСТОК)').each(function(i, el){
				var $el = $(el)
				$el.appendTo(doc);
			});
		}, 'html');
	}
});