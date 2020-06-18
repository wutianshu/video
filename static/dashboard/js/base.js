window.onload = function () {
    // var videoStatus = false;
    // $('#video-form-area').hide();
    // $('#videoid').on('click', function () {
    //     if (!videoStatus) {
    //         $('#video-form-area').show();
    //         videoStatus = true;
    //     } else {
    //         $('#video-form-area').hide();
    //         videoStatus = false;
    //     }
    // });

    $('#video-create-form').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var videoid = button.data('video-id');
        var videoname = button.data('video-name');
        var videoimage = button.data('video-image');
        var videotype = button.data('video-type');
        var videoorigin = button.data('video-origin');
        var videonationality = button.data('video-nationlity');

        var modal = $(this);
        modal.find('#video_id').val(videoid);
        modal.find('#video_name').val(videoname);
        modal.find('#video_image').val(videoimage);
        modal.find('#video_type').val(videotype);
        modal.find('#video_origin').val(videoorigin);
        modal.find('#video_nationality').val(videonationality);
    });

    var urlStatus = false;
    $('#file-form-area').hide();
    $('#file_addr').on('click', function () {
        if (!urlStatus) {
            $('#file-form-area').show();
            urlStatus = true;
        } else {
            $('#file-form-area').hide();
            urlStatus = false;
        }
    });

    var actorStatus = false;
    $('#actor-form-area').hide();
    $('#actor_info').on('click', function () {
        if (!actorStatus) {
            $('#actor-form-area').show();
            actorStatus = true;
        } else {
            $('#actor-form-area').hide();
            actorStatus = false;
        }
    });


    $('#exampleModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        var videosubId = button.data('id');
        var videoSubNumber = parseInt(button.data('number'));
        var videoSubUrl = button.data('url');
        var videoId = button.data("videoid");
        modal.find('#videoid').val(videoId); //视频id
        modal.find('#videofileid').val(videosubId); //视频文件id
        modal.find('#videonumber').val(videoSubNumber);
        modal.find('#videlurl').val(videoSubUrl);
    })

};