$(document).ready(function(){
    $("#delete-all-button").click(function(){
       $.ajax({
           type: 'DELETE',
           url: '/api/images',
           success: function () {
               window.location.href = '/';
               toastr.success('All images deleted');
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
                toastr.success('Image deleted');
            }
        })
    })

    $(".open-prompt-button").click(function() {
        const $this = $(this);
        const id = $this.data('id');
        window.location.href = `/?prompt_id=${id}`;
    })
})