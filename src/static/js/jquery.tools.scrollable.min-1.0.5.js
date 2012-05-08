/*
 * jquery.tools 1.0.2 - The missing UI library
 * 
 * [tools.scrollable-1.0.5]
 * 
 * Copyright (c) 2009 Tero Piirainen
 * http://flowplayer.org/tools/
 *
 * Dual licensed under MIT and GPL 2+ licenses
 * http://www.opensource.org/licenses
 * 
 * -----
 * 
 * Build: Fri Jun 12 13:55:52 GMT+00:00 2009
 */
(function(b){b.tools=b.tools||{version:{}};b.tools.version.scrollable="1.0.5";var c=null;function a(p,m){var s=this;if(!c){c=s}function n(t,u){b(s).bind(t,function(w,v){if(u&&u.call(this,v.index)===false&&v){v.proceed=false}});return s}b.each(m,function(t,u){if(b.isFunction(u)){n(t,u)}});var d=!m.vertical;var f=b(m.items,p);var j=0;function l(u,t){return u.indexOf("#")!=-1?b(u).eq(0):t.siblings(u).eq(0)}var q=l(m.navi,p);var g=l(m.prev,p);var i=l(m.next,p);var h=l(m.prevPage,p);var o=l(m.nextPage,p);b.extend(s,{getIndex:function(){return j},getConf:function(){return m},getSize:function(){return s.getItems().size()},getPageAmount:function(){return Math.ceil(this.getSize()/m.size)},getPageIndex:function(){return Math.ceil(j/m.size)},getRoot:function(){return p},getItemWrap:function(){return f},getItems:function(){return f.children()},getVisibleItems:function(){return s.getItems().slice(j,j+m.size)},seekTo:function(w,u,A){if(u===undefined){u=m.speed}if(b.isFunction(u)){A=u;u=m.speed}if(w<0){w=0}if(w>s.getSize()-m.size){return s}var B=s.getItems().eq(w);if(!B.length){return s}var t={index:w,proceed:true};b(s).trigger("onBeforeSeek",t);if(!t.proceed){return s}if(d){var v=-B.position().left;f.animate({left:v},u,m.easing,A?function(){A.call(s)}:null)}else{var z=-B.position().top;f.animate({top:z},u,m.easing,A?function(){A.call(s)}:null)}if(q.length){var x=m.activeClass;var y=Math.ceil(w/m.size);y=Math.min(y,q.children().length-1);q.children().removeClass(x).eq(y).addClass(x)}if(w===0){g.add(h).addClass(m.disabledClass)}else{g.add(h).removeClass(m.disabledClass)}if(w>=s.getSize()-m.size){i.add(o).addClass(m.disabledClass)}else{i.add(o).removeClass(m.disabledClass)}c=s;j=w;b(s).trigger("onSeek",{index:w});return s},move:function(v,u,t){var w=j+v;if(m.loop&&w>(s.getSize()-m.size)){w=0}return this.seekTo(w,u,t)},next:function(u,t){return this.move(1,u,t)},prev:function(u,t){return this.move(-1,u,t)},movePage:function(v,u,t){return this.move(m.size*v,u,t)},setPage:function(x,y,v){var u=m.size;var t=u*x;var w=t+u>=this.getSize();if(w){t=this.getSize()-m.size}return this.seekTo(t,y,v)},prevPage:function(u,t){return this.setPage(this.getPageIndex()-1,u,t)},nextPage:function(u,t){return this.setPage(this.getPageIndex()+1,u,t)},begin:function(u,t){return this.seekTo(0,u,t)},end:function(u,t){return this.seekTo(this.getSize()-m.size,u,t)},reload:function(){return r()},click:function(u,x,v){var w=s.getItems().eq(u);var t=m.activeClass;if(u<0||u>=this.getSize()){return s}if(m.size==2){if(u==s.getIndex()){u--}s.getItems().removeClass(t);w.addClass(t);return this.seekTo(u,x,v)}if(!w.hasClass(t)){s.getItems().removeClass(t);w.addClass(t);var z=Math.floor(m.size/2);var y=u-z;if(y>s.getSize()-m.size){y=s.getSize()-m.size}if(y!==u){return this.seekTo(y,x,v)}}return s},onBeforeSeek:function(t){return n("onBeforeSeek",t)},onSeek:function(t){return n("onSeek",t)}});if(b.isFunction(b.fn.mousewheel)){p.bind("mousewheel.scrollable",function(u,v){var t=b.browser.opera?1:-1;s.move(v>0?t:-t,50);return false})}g.addClass(m.disabledClass).click(function(){s.prev()});i.click(function(){s.next()});o.click(function(){s.nextPage()});h.addClass(m.disabledClass).click(function(){s.prevPage()});if(m.keyboard){b(document).unbind("keydown.scrollable").bind("keydown.scrollable",function(t){var u=c;if(!u||t.altKey||t.ctrlKey){return}if(d&&(t.keyCode==37||t.keyCode==39)){u.move(t.keyCode==37?-1:1);return t.preventDefault()}if(!d&&(t.keyCode==38||t.keyCode==40)){u.move(t.keyCode==38?-1:1);return t.preventDefault()}return true})}function r(){if(q.is(":empty")||q.data("me")==s){q.empty();q.data("me",s);for(var u=0;u<s.getPageAmount();u++){var v=b("<"+m.naviItem+"/>").attr("href",u).click(function(x){var w=b(this);w.parent().children().removeClass(m.activeClass);w.addClass(m.activeClass);s.setPage(w.attr("href"));return x.preventDefault()});if(u===0){v.addClass(m.activeClass)}q.append(v)}}else{var t=q.children();t.each(function(w){var x=b(this);x.attr("href",w);if(w===0){x.addClass(m.activeClass)}x.click(function(){q.find("."+m.activeClass).removeClass(m.activeClass);x.addClass(m.activeClass);s.setPage(x.attr("href"))})})}if(m.clickable){s.getItems().each(function(x,w){var y=b(this);if(!y.data("set")){y.bind("click.scrollable",function(){s.click(x)});y.data("set",true)}})}if(m.hoverClass){s.getItems().hover(function(){b(this).addClass(m.hoverClass)},function(){b(this).removeClass(m.hoverClass)})}return s}r();var e=null;function k(){if(e){return}e=setInterval(function(){if(m.interval===0){clearInterval(e);e=0;return}s.next()},m.interval)}if(m.interval>0){p.hover(function(){clearInterval(e);e=0},function(){k()});k()}}b.fn.scrollable=function(d){var e=this.eq(typeof d=="number"?d:0).data("scrollable");if(e){return e}var f={size:5,vertical:false,clickable:true,loop:false,interval:0,speed:400,keyboard:true,activeClass:"active",disabledClass:"disabled",hoverClass:null,easing:"swing",items:".items",prev:".prev",next:".next",prevPage:".prevPage",nextPage:".nextPage",navi:".navi",naviItem:"a",api:false,onBeforeSeek:null,onSeek:null};b.extend(f,d);this.each(function(){e=new a(b(this),f);b(this).data("scrollable",e)});return f.api?e:this}})(jQuery);
