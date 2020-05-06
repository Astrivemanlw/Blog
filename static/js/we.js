// function jump(page_num) {
//     $.get('/page_ajax/' + page_num, function (data) {
//         //通过 '[id = blog_title]' 获取所有同ID元素 外层引号不能少 否则只能取到第一个元素
//         $('[id = blog_title]').each(function (i) {
//             $(this).html(data.blog_title[i])
//
//         });
//         $('[id = blog_timestamp]').each(function (i) {
//             $(this).html(data.blog_timestamp[i])
//
//         });
//         $('[id = blog_content]').each(function (i) {
//
//             $(this).html(data.blog_content[i])
//
//         })
//     })
// }

function jump_link(url) {
    window.location.href = url
}

//搜索框
function search() {
    jump_link('/search?key_word=' + $('#key_word').val())
}

// 按钮绑定回车
$("body").keydown(function () {
    if (event.keyCode == "13") {//keyCode=13是回车键
        search()
    }
});

//moment时间渲染
$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }

    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});

let has_been_liked = false;
let has_been_not_liked = false;
// 赞fa fa-thumbs-o-up
//取消赞 fa-thumbs-up fa
//踩 fa-thumbs-down fa
//取消踩  fa fa-thumbs-o-down
function like_change(obj) {
    let post_id = $(obj).prev().attr('id');
    let love_cn = $(obj).find("span").text();
    let love_cn_add = Number(love_cn) + 1;
    let love_cn_min = Number(love_cn) - 1;
    $.get('/manage/sync_like_cn?post_id=' + post_id + "&love_cn_add=" + love_cn_add, function () {
    });
    $(obj).parent().find("#not_like").attr({"class": "fa fa-thumbs-o-down"});
    $(obj).children().toggleClass("fa fa-thumbs-up");
    $(obj).children().toggleClass("fa fa-thumbs-o-up");
    //赞 点赞数+1
    if (!has_been_liked) {
        $(obj).find("span").text(love_cn_add);
        has_been_liked = true;
        has_been_not_liked = false
    // 取消点赞
    } else {
        $(obj).find("span").text(love_cn_min);
        has_been_liked = false
        has_been_not_liked = true
    }
}


function not_like_change(obj) {
    let love_cn = $(obj).parent().find("#like").find("span").text();
    $(obj).parent().find("#like").attr({"class": "fa fa-thumbs-o-up"});
    $(obj).children().toggleClass("fa fa-thumbs-down");
    $(obj).children().toggleClass("fa fa-thumbs-o-down");
    // 踩 点赞数-1
    if (!has_been_not_liked && has_been_liked) {
        $(obj).parent().find("#like").find("span").text(Number(love_cn) - 1);
        has_been_not_liked = true;
        has_been_liked = false
    }
}

function reply(obj) {

    let btn_val = $(obj).text().trim();
    let action = 0;
    let comment_id = $(obj).parent().parent().attr('id');
    if (btn_val == '修改') {
        action = 1;
        comment_id = $(obj).parent().parent().parent().attr('id');
    }
    let form_div = "<form action=\"/manage/reply_comment?comment_id=" + comment_id + "&action=" + action +
        "\" id=reply_form_id method=\"post\" class=\"form\" role=\"form\"><input id=\"csrf_token\" name=\"csrf_token\" type=\"hidden\" value=" + csrf_token_val +
        "><div class=\"form-group\"><label class=\"form-control-label\" for=\"comment\"></label><textarea class=\"form-control\" id=\"content\" name=\"content\"></textarea></div><input class=\"btn btn-primary\" id=\"submit\" name=\"submit\" type=\"submit\" value=\"发表\"></form>"
    if (btn_val == '回复' || btn_val == '修改') {
        console.log(form_div)

        $(obj).parent().after(form_div);
        $(obj).html('<i class="fa fa-caret-down"></i>&nbsp;收起');
    }

    if (btn_val == '收起') {
        $(obj).parent().parent().find('#reply_form_id').remove();
        $(obj).html('<i class="fa fa-reply"></i>&nbsp;&nbsp;回复');

    }

}

function look_reply(obj) {
    let btn_val = $(obj).text().trim();
    let cmt_id = $(obj).parent().parent().attr('id')
    let admin_btn = "<small class =\"float-right\">" +
        "                <button  id=\"reply\" class=\"btn btn-primary btn-sm\" onclick=\"reply(this)\"> <i class=\"fa fa-pencil\"></i>修改</button> " +
        "<button   id=\"reply\" class=\"btn btn-danger btn-sm\" onclick=\"delete_reply(this);\"> <i class=\"fa fa-minus-square\">  删除</i></button>" +
        "</small>"

    $.get('/manage/get_reply_data?comment_id=' + cmt_id, function (reply_data) {
            console.log(reply_data);
            if (btn_val == "查看回复") {
                if (current_user_is_admin == "False") {
                    admin_btn = "";
                }
                $(obj).parent().after("<div id='reply_content'><hr>&nbsp;&nbsp;&nbsp;&nbsp;作者回复: " + reply_data + admin_btn + "<p></p></div>");
                $(obj).html('<i class="fa fa-caret-down"></i>&nbsp;收起');

            }

            if (btn_val == '收起') {
                $("#reply_content").remove();
                $(obj).html('<i class="fa fa-eye"></i>&nbsp;查看回复');

            }
        }
    )
}

function delete_comment(obj) {
    let do_delete = confirm('确定删除评论及其回复吗?');
    let cmt_obj = $(obj).parent().parent();
    if (do_delete == true) {
        let comment_id = cmt_obj.attr("id");
        $.get('/manage/delete_comment?comment_id=' + comment_id, function () {
            console.log(cmt_obj.parent().find('.fa-comment'));
            cmt_obj.parent().find('.fa-comment').before(flash_ajax('删除成功'))
            cmt_obj.remove()

        })
    }
}

function delete_reply(obj) {
    let do_delete = confirm('确定该回复吗?');
    let reply_obj = $(obj).parent().parent();
    let cmt_obj = reply_obj.parent();
    let reply_btn = reply_obj.prev();
    console.log()
    if (do_delete == true) {
        let comment_id = cmt_obj.attr("id");
        $.get('/manage/delete_reply?comment_id=' + comment_id, function () {
            cmt_obj.parent().find('.fa-comment').before(flash_ajax('删除成功'));
            reply_obj.remove()
            $(reply_btn).html("<button value=\"reply\" id=\"reply\" class=\"btn btn-primary btn-sm\" onclick=\"reply(this)\">  <i class=\"fa fa-reply\"></i>&nbsp;&nbsp;回复 </button>")

        })
    }
}


function flash_ajax(msg) {
    return "<div class=\"alert alert-info\"> <button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>" + msg + "</div>"
}

function changeFunc() {
    console.log($('#catalog option:selected').text() == '阅读')
    if ($('#catalog option:selected').text() == '阅读') {
        console.log('come in')
        $('#catalog').after("<div class=\"form-group required\"><input class=\"form-control\" id=\"title\" name=\"title\" required=\"\" type=\"text\" value=\"\"> </div>");
        //$('#catalog').remove();
    }

}

$(function () {
    $('#catalog').attr({"onchange": "changeFunc()"});

})

