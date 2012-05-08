/*
	Ticker Plugin
	Copyright (c) 2012 Andrey Gavrilov / www.andrgavr.com
	Released under MIT License
	--------------------------
	Structure based on Zach Dunn's Totem Ticker jQuery plugin
*/
(function( $ ){
	
	if(!$.omr){
		$.omr = new Object();
	};
	
	$.omr.ticker = function(el, options ) {
	  	
	  	var base = this;
		
		var ic

	  	
		//Define the DOM elements
	  	base.el = el;
	  	base.$el = $(el);
		
	  	
	  	// Add a reverse reference to the DOM object
        base.$el.data("omr.ticker", base);
	  	
	  	base.init = function(){
            base.options = $.extend({},$.omr.ticker.defaultOptions, options);
            
            //Define the ticker object
           	base.ticker;
			
			ic = base.$el.html();
			
			//Adjust the height of ticker if specified
			base.format_ticker();
			
			base.setup_nav();
			
			//Stopping the ticker on init
			base.stop_interval();
			
			//Debugging info in console
			//base.debug_info();
        };
		
		base.start_interval = function(){
			
			//Clear out any existing interval
			clearInterval(base.ticker);

	

	    	base.ticker = setInterval(function() {
	    	
	    		base.$el.find('li:first').animate({
	            	marginTop: '-' + base.options.row_height,
	            }, base.options.speed, 'easeOutElastic', function() {
	                $(this).detach().css('marginTop', '0').appendTo(base.$el);
	            });
	            
	    	}, base.options.interval);
	    }
	    
    
	    base.stop_interval = function(){
	    	clearInterval(base.ticker);
			base.$el.html(ic);
			
	    }
	
		base.format_ticker = function(){
		
			if(typeof(base.options.max_items) != "undefined" && base.options.max_items != null) {
				
				//Remove units of measurement
				var stripped_height = base.options.row_height.replace(/px/i, '');
				var ticker_height = stripped_height * base.options.max_items;
			
				base.$el.css({
					height		: ticker_height + 'px', 
					overflow	: 'hidden',	
				});
				
			}else{
				//No heights were specified, so just doublecheck overflow = hidden
				base.$el.css({
					overflow	: 'hidden',
				})
			}
			
		}
	
		base.setup_nav = function(){
			//Start on mouse hover
			if (typeof(base.options.hob) != "undefined" && base.options.hob != null){
				// If receiver object is specified track mouse events for it
				$(base.options.hob).mouseover(function(){
					base.start_interval();
				}).mouseleave(function(){
					base.stop_interval();
				});
			} else {			
				// If receiver object isn't specified use ticker itself
				base.$el.mouseover(function(){
					base.start_interval();
				}).mouseleave(function(){
					base.stop_interval();
				});
		
			}
			

			
		}
		
		
/*		base.debug_info = function()
		{
			//Dump options into console
			console.log(base.options);
		}*/
		
		//Make it go!
		base.init();
		

		
  };
  
  $.omr.ticker.defaultOptions = {
  		row_height	:	'100px',	/* Height of each ticker row in PX. Should be uniform. */
  		speed		:	400,		/* Speed of transition animation in milliseconds */
  		interval	:	1000,		/* Time between change in milliseconds */
		max_items	: 	null, 		/* Integer for how many items to display at once. Resizes height accordingly (OPTIONAL) */
		hob			:	null		/* Receiver Object for firing the scroll start*/
  };
  
  $.fn.ticker = function( options ){
    return this.each(function(){
    	(new $.omr.ticker(this, options));
  	});
  };
  
})( jQuery );