$(".navHover1").hover(
    function (){
        $(".navHoverItem1").show();
},  function () {
        $(".navHoverItem1").hide();
});

$(".navHoverItem1").hover(
    function () {
        $(this).show();//鼠标进入下拉框
},  function () {
        $(this).hide();//鼠标离开下拉框后，就会消失
});

$(".navHover2").hover(
    function (){
        $(".navHoverItem2").show();
},  function () {
        $(".navHoverItem2").hide();
});

$(".navHoverItem2").hover(
    function () {
        $(this).show();//鼠标进入下拉框
},  function () {
        $(this).hide();//鼠标离开下拉框后，就会消失
});

// 向上滚动的函数
$(function () {
    $('#BackTop').click(function () {
        $('html,body').animate({scrollTop: 0}, 500);
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#BackTop').fadeIn(300);
        } else {
            $('#BackTop').stop().fadeOut(300);
        }
    }).scroll();
});

//标签颜色
$(function () {
    let colorList = ['#F65087','#329768','#FB8052','#3693CA','#68C999','#109691'];

    $('.sort li').each(function (i) {
        $(this).css({background:colorList[i%5]});
    });
});

$(function () {
    if (location.pathname === '/'){
        $('#home').addClass('active');
    }else if (location.pathname.search(/category/i) != -1 || location.pathname.search(/tag/i) != -1 || location.pathname.search(/article/i) != -1){
        if ($('#art').attr('class').search(/active/) === -1){
            $('#art').addClass('active');
        }
    }else if (location.pathname.search(/about/i) != -1){
        if ($('#about').attr('class').search(/active/) === -1){
            $('#about').addClass('active');
        }
    }
});

$(function () {
    $('[data-toggle="popover"]').popover();
});