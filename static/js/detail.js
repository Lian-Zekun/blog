// 粘性侧边栏
$('#sidebar').stickySidebar({
//    containerSelector: '#art-content',
    topSpacing: 66,
    bottomSpacing: 56,
    innerWrapperSelector: '.sidebar__inner',
});

$(function () {
    $('.toc a').addClass('hvr-forward no-underline')
})

function load_modal(article_id, comment_id) {
    let modal_body = '#modal_body_' + comment_id;
    let modal_id = '#reply_' + comment_id;

    // 加载编辑器
    if ($(modal_body).children().length === 0) {
        let content = '<iframe src="/api/comment/post-comment/'
            +article_id+
            '/'
            +comment_id+
            '"' + ' frameborder="0" style="width: 100%; height: 100%;" id="iframe_'
            +comment_id+
            '"></iframe>';
        $(modal_body).append(content);
    };

    $(modal_id).modal('show');
}

// 锚点定位
function post_reply_and_show_it(article_id, new_comment_id) {
    let next_url = '/article/' + article_id;
    // 去除 url 尾部 '/' 符号
    next_url = next_url.charAt(next_url.length - 1) == '/' ? next_url.slice(0, -1) : next_url;
    // 刷新并定位到锚点
    window.location.replace(next_url + "#comment_" + new_comment_id);
};

// 展开根评论 height <= 500px 时
const unfoldContent = (node_id) => {
    const comment_body = $("#comment_body_" + node_id);
    const link_elem = $(".link_elem_" + node_id);
    if (comment_body.height() <= 500) {
        comment_body.css('max-height', '');
        link_elem.hide();
    }
};

// 展开根评论及子评论
const onUnfoldContent = (self, node_id) => {
    if ($(self).attr('aria-expanded') === 'false') {
        unfoldContent(node_id);
        $(self).text("折叠此评论..")
    }else {
        $(self).text("展开此评论..")
    }
};

$(function () {
    // 展开根评论
    const comment_body_divs = $('div#comment_body_div');
    const unfold_links = $('a#unfold_link');
    for (const div of comment_body_divs) {
        let comment_body_height = $(div).children('.comment-hidden').height();
        if (comment_body_height < 500) {
            $(div).children('div#gradient_layer').hide();
        }
    }
    // 子评论解除隐藏
    const children_comments = $('.children').find('.comment-hidden').css('max-height', '');

    // 展开/渲染评论锚点
    const aQuery = window.location.href.split("#")[1];
    const comment_selector = $('#' + aQuery);
    comment_selector.parents('.collapse').collapse();
    comment_selector.attr('style', 'border-left: 4px solid #FF8C00');
});

// 进度条
$(function() {
    var getMax = function(){
        return $('.center_content').height() - $(window).height();
    }

    var getValue = function(){
        return $(window).scrollTop();
    }

    if ('max' in document.createElement('progress')) {
        // Browser supports progress element
        var progressBar = $('progress');

        // Set the Max attr for the first time
        progressBar.attr({ max: getMax() });

        $(document).on('scroll', function(){
            // On scroll only Value attr needs to be calculated
            progressBar.attr({ value: getValue() });
        });

        $(window).resize(function(){
            // On resize, both Max/Value attr needs to be calculated
            progressBar.attr({ max: getMax(), value: getValue() });
        });

    } else {

        var progressBar = $('.progress-bar'),
            max = getMax(),
            value, width;

        var getWidth = function() {
            // Calculate width in percentage
            value = getValue();
            width = (value/max) * 100;
            width = width + '%';
            return width;
        }

        var setWidth = function(){
            progressBar.css({ width: getWidth() });
        }

        $(document).on('scroll', setWidth);
        $(window).on('resize', function(){
            // Need to reset the Max attr
            max = getMax();
            setWidth();
        });
    }
});
