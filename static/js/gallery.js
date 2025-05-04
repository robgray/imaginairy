$(document).ready(function(){
    $("#delete-all-button").click(function(){
       $.ajax({
           type: 'DELETE',
           url: '/api/images',
           success: function () {
               window.location.href = '/';
           }
       })
    });

    $(".delete-image-button").click(function() {
        const $this = $(this);
        const id = $this.data('id');
        $.ajax({
            type: 'DELETE',
            url: `/api/images/${id}` ,
            success: function () {
                $(`.${id}`).remove();
            }
        })
    })

    $(".open-prompt-button").click(function() {
        const $this = $(this);
        const id = $this.data('id');
        window.location.href = `/?prompt_id=${id}`;
    })
})