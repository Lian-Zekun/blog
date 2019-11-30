$(".django-ckeditor-widget").removeAttr('style');

function confirm_submit(article_id, parent_comment_id){
    if ($("#reply_form").length > 0) {
        // 从 ckeditor 中取值
        let content = CKEDITOR.instances['id_content'].getData();
        // 调用 ajax 与后端交换数据
        $.ajax({
            type: 'POST',
            url: '/api/comment/post-comment/' + article_id + '/' + parent_comment_id,
            data: {'content': content},
            // 成功回调
            success: function(e){
                if(e.code === '200 OK'){
                    parent.post_reply_and_show_it(article_id, e.new_comment_id);
            }
        }
        });
    }
}