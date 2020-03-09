let getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

let $ingredientsSearch = $('#ingredients-search');


let options = {
    selected_symbol_type: 'fontawesome_star',
    max_value: 5,
    step_size: 1
};

let $body = $('body');
let $signInModal = $('#sign-in-modal');
let searchInputTimer;

$('.rating').rate(options);

let getSearchResults = () => {
    let url = $ingredientsSearch.attr('data-url') + '?query=' + $ingredientsSearch.val();
    $.ajax({
        url: url,
        success: (data) => {
            $('#searched-recipes').html(data.html);
        }
    })
};

$ingredientsSearch.on('keyup', function (e) {
    clearTimeout(searchInputTimer);
    searchInputTimer = setTimeout(getSearchResults, 500);
});

$body.on('click', '#sign-in-modal-btn', function (e) {
    e.preventDefault();
    window.location = $(this).attr('data-url') + '?next=' + window.location.pathname;
});

$body.on('click', '#search-input-submit', function (e) {
    e.preventDefault();
    getSearchResults()
});

$body.on('change', '.rating', function (event, data) {
    let $this = $(this);
    let recipeId = $this.attr('data-recipe-id');
    let userId = $this.attr('data-user-id');
    let url = $this.attr('data-url');
    console.log(userId);

    if (userId) {
        $.ajax({
            url: url,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            method: "post",
            data: {
                recipe_id: recipeId,
                rating: data.to
            },
            success: function (data) {
                $this.parents('article').first().find('.rating-info').html(data.rating_info);
                if (data.success) {
                    toastr['success'](data.message);
                } else {
                    toastr['warning'](data.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        $signInModal.modal('show');
    }
});

$body.on('click', '.recipe-comments-show', function (e) {
    e.preventDefault();
    let $this = $(this);
    let recipeId = $this.attr('data-recipe-id');
    let userId = $this.attr('data-user-id');

    let dataTarget = $(this).attr('data-target');
    $.ajax({
        url: $this.attr('data-url'),
        success: (data) => {
            $(dataTarget).find('.previous-comments').html(data);
        }
    });

    $.ajax({
        url: $this.attr('data-form-url'),
        success: (data) => {

            let $data = $(data);

            $data.find("input[name='recipe']").val(recipeId);
            $data.find("input[name='created_by']").val(userId);
            $(dataTarget).find('.comment-form-container').append($data);

        }
    })
});

$body.on('click', '.post-comments-show', function (e) {
    e.preventDefault();
    let $this = $(this);
    let postId = $this.attr('data-post-id');
    let userId = $this.attr('data-user-id');

    let dataTarget = $(this).attr('data-target');
    $.ajax({
        url: $this.attr('data-url'),
        success: (data) => {
            $(dataTarget).find('.previous-comments').html(data);
        }
    });

    $.ajax({
        url: $this.attr('data-form-url'),
        success: (data) => {

            let $data = $(data);

            $data.find("input[name='post']").val(postId);
            $data.find("input[name='created_by']").val(userId);
            $(dataTarget).find('.comment-form-container').append($data);

        }
    })
});

$.endlessPaginate({
    onClick: function () {
    }
});

$body.on('submit', '.comment-form', function (e) {
    e.preventDefault();
    let $this = $(this);
    let userId = $this.find("input[name='created_by']").val();
    if (userId) {
        $.ajax({
            url: $this.attr('action'),
            method: "post",
            data: $this.serialize(),
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            success: (data) => {
                if (data.success) {
                    $this.parents('article').first().find('.new-comments').append(data.html);
                    $this.parents('article').first().find('.comments-count').find('span').html(data.comments_count + ' ');
                    toastr['success'](data.message);
                    $this[0].reset();
                } else {

                    let errors = JSON.parse(data.errors);
                    Object.entries(errors).map(entry => {
                        toastr['warning'](entry[0] + ": " + entry[1][0].message)
                    })
                }

            },
            error: (error) => {
                console.log(error);
            }
        })
    } else {
        $signInModal.modal('show');
    }
})