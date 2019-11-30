$(function () {
    go_to_page(1);
    //选择所有的页码绑定点击事件
    function page_click(){
        $('.pages a:not(":first,:last")').click(function () {
            page_num=$(this).text();     //page_num为接下来要请求的页码号
            go_to_page(page_num);
        });
    }
    function GetQueryString(name){
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if(r!=null) return decodeURI(r[2]); return null;
    }
    function go_to_page(page_num) {      //ajax刷新当前页面文章   page_num为接下来要请求的页码号
        if (location.pathname.search(/search/i) != -1){
            var url = '/api/search';
            var page = GetQueryString('page');
            if (page) {
                var data = {'q':GetQueryString('q'), 'page':GetQueryString('page')};
            } else {
                var data = {'q':GetQueryString('q')};
            }
        } else {
            var url = '/api';
            var data = {'page_num':page_num, 'path':location.pathname};
        }
        $.ajax({
            type: 'GET',
            data: data,
            url: url,
            datatype:JSON,      //希望返回Json格式的数据
            success:function (data) {
                f1(data);     //处理返回后的数据
            },
            error:function () {
                console.log('ajax刷新分页数据失败！');
            }
        })
    }
    function f1(data) {   //处理返回后的数据    data为字符串型
        data = $.parseJSON(data);    //将字符串型转化为object
        //刷新文章
        if (data.result.length != 0){
            $('.timeline li').remove();
            for (var i = 0; i < data.result.length; i++) {
                $('.timeline').append('<li><div class="row"><div class="col-sm-2 col-md-2 col-lg-2 col-xl-3"><time class="tmtime"><span><h3>'
                    +data.result[i][0]+
                    '</h3></span><span><h3>'
                     +data.result[i][1]+
                    '</h3></span></time><div class="tmicon"></div></div><div class="col-sm-10 col-md-10 col-lg-10 col-xl-9"><div class="tmlabel"><h3><a href="/article/'
                    +data.result[i][6]+
                    '">'
                    +data.result[i][2]+
                    '</a></h3><div class="row"><img src="/media/'
                    +data.result[i][3]+
                    '" class="col-sm-4 img-responsive blogpic"><div class="col-sm-8">'
                    +data.result[i][4]+
                    '<p><span><i class="fas fa-eye" style="color: #444;"></i>'
                    +data.result[i][5]+
                    '&nbsp;&nbsp;&nbsp;</span></p></div></div></div></div></div></li>'
                );
            }
        } else {
            console.log(1);
            $('.timeline li').remove();
            $('.timeline').append('<h3 style="text-align: center">没有找到相关文章<h3>');
        }
        //刷新页码
        $('.pages a:not(":first,:last")').remove();
        $('.pages span').remove();
        if(parseInt(data.num_pages) <= 7) {     //如果总页码数小于等于8
            for(var i=1;i<=parseInt(data.num_pages);i++){
                $('.pages a:last').before('<a href="javascript:;" class="page-number">' +i+ '</a>');
            }
        }else if(parseInt(data.page_num) <= 4){        //如果当前页码数小于等于4
            for(var i=1;i<=parseInt(data.page_num)+2;i++){
                $('.pages a:last').before('<a href="javascript:;" class="page-number">' +i+ '</a>');
            }
            $('.pages a:last').before('<span class="space">…</span>');
            $('.pages a:last').before('<a href="javascript:;" class="page-number">' +data.num_pages+ '</a>');
        }else if(parseInt(data.page_num)>=parseInt(data.num_pages)-3){    //当前页后面不足4页时
            $('.pages a:last').before('<a href="javascript:;" class="page-number">1</a>');
            $('.pages a:last').before('<span class="space">…</span>');
            for(var i=parseInt(data.page_num)-2;i<=parseInt(data.num_pages);i++){
                $('.pages a:last').before('<a href="javascript:;" class="page-number">' +i+ '</a>');
            }
        }else{
            $('.pages a:last').before('<a href="javascript:;" class="page-number">1</a>');
            $('.pages a:last').before('<span class="space">…</span>');
            for(var i=-2;i<=2;i++){
                $('.pages a:last').before('<a href="javascript:;" class="page-number">' +(parseInt(data.page_num)+i)+ '</a>');
            }
            $('.pages a:last').before('<span class="space">…</span>');
            $('.pages a:last').before('<a href="javascript:;" class="page-number">' +data.num_pages+ '</a>');
        }
        $('.pages a:not(":first,:last")').each(function () {    //为当前页加上active
            if($(this).text()==data.page_num)
                $(this).addClass('active');
        });
        page_click();   //为刷新后的页码绑定点击事件
        $('.pages a:first').unbind("click").click(function () {
            if(parseInt(data.page_num)>1) {
                go_to_page(parseInt(data.page_num)-1);
            }
        });
        $('.pages a:last').unbind("click").click(function () {
            if(parseInt(data.page_num)<parseInt(data.num_pages)){
                go_to_page(parseInt(data.page_num)+1);
               }
        });
    }
});