// 评论适应宽度
$(".django-ckeditor-widget").removeAttr('style');

// 限制评论频率和篇幅
const submit_comment = () => {
    if ($("#comment_form").length > 0 || $("#reply_form").length > 0) {
        let contentLength = CKEDITOR.instances['id_content']
            .getData()
            .replace(/<img[^>]+>/g, 'I')
            .replace(/<[^>]+>/g, '')
            .replace(/&nbsp;/g, 'X')
            .replace(/\s/g, '')
            .length;

        if (contentLength <= 0) {
            alert('留言不能为空哦~');
        } else if (contentLength > 3000) {
            alert('评论篇幅请小于3000字哟~');
        } else {
            $('#comment_submit').trigger('click');
        }
    }
};

// 显示评论字数
$(() => {
    if ($("#comment_form").length > 0 || $("#reply_form").length > 0) {
        let ckeditor = CKEDITOR.instances['id_content'];

        let comment_char_count = $('#comment_char_count');
        ckeditor.on('change', () => {
            let contentLength = CKEDITOR.instances['id_content']
                .getData()
                .replace(/<img[^>]+>/g, 'I')
                .replace(/<[^>]+>/g, '')
                .replace(/&nbsp;/g, 'X')
                .replace(/\s/g, '')
                .length;

            if (contentLength < 3000) {
                comment_char_count.html(contentLength + '字')
                    .stop()
                    .removeAttr('style')
                    .fadeOut(3000);
            } else {
                comment_char_count.html('<span style="color: red;">' + contentLength + '</span>' + '/3000字')
                    .stop()
                    .removeAttr('style');
            }
        });
    }
});