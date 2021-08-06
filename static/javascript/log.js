layui.use('carousel', function(){
    var carousel = layui.carousel;
    carousel.render({
      elem: '#test1'
      ,width: '100%' 
      ,height: '480px'
      ,arrow: 'always' 
      ,indicator:'outside'

    });
  });