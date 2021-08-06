layui.use('element', function(){
var element = layui.element; 
element.on('nav(demo)', function(elem){
layer.msg(elem.text());
});
});


function initialize()
{
var mapProp = {
center:new google.maps.LatLng(55.86549,-4.25409),
zoom:15,
mapTypeId:google.maps.MapTypeId.ROADMAP
};
var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
}

google.maps.event.addDomListener(window, 'load', initialize);