$(document).ready(() => {
    $('.btn.btn-primary').click(() => {
        sendAjaxForm('my-form', 'http://localhost:8000/api/v0/addlink/')
    })
});

function sendAjaxForm(ajax_form, url) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'html',
        data: $('#' + ajax_form).serialize(),
        success: (response) => {
            a = $('#div-form');
            a.append(
                "<div class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">\n" +
                "<h4 class=\"alert-heading\">Good!</h4>\n" +
                "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
                "<span aria-hidden=\"true\">&times;</span>\n" +
                "</button>\n" +
                "</div>"
            )
        },
        error: (response) => {
            a = $('#div-form');
            a.append(
                "<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">\n" +
                "<h4 class=\"alert-heading\">Something went wrong((</h4>\n" +
                "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
                "<span aria-hidden=\"true\">&times;</span>\n" +
                "</button>\n" +
                "</div>"
            )
        }
    });
}