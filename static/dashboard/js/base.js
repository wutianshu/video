

window.onload=function () {
    var videoStatus = false;
    $('#video-form-area').hide();
    $('#videoid').on('click', function () {
    if(!videoStatus){
        $('#video-form-area').show();
        videoStatus=true;
    }else {
        $('#video-form-area').hide();
        videoStatus=false;
    }
});
};