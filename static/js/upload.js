const uploadForm = document.getElementById('upload_form');
const input_file = document.getElementById('id_local_file');
const progress_bar = document.getElementById('progress');
const progress_text = document.getElementById('percents');

$("#upload_form").submit(function (e) {
    e.preventDefault();
    $form = $(this);
    let formData = new FormData(this);
    const media_data = input_file.files[0];
    if (media_data != null) {
        console.log(media_data);
        progress_bar.classList.remove("not-visible");
    }

    $.ajax({
        type: 'POST',
        url: '',
        data: formData,
        dataType: 'json',
        beforeSend: function () {

        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if (e.lengthComputable) {
                    const percentProgress = (e.loaded / e.total) * 100;
                    console.log(percentProgress);
                    progress_bar.setAttribute('value', `${percentProgress}`);
                    progress_text.innerText = `${percentProgress.toFixed(2)}/100%`;
                }
            });
            return xhr
        },
        success: function (response) {
            console.log(response);
            uploadForm.reset();
            progress_bar.classList.add('not-visible');
        },
        error: function (err) {
            console.log(err);
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});
