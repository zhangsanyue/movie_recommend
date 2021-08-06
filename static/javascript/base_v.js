layui.use('element', function(){
    var element = layui.element; 
    element.on('nav(demo)', function(elem){
    layer.msg(elem.text());
    });
});