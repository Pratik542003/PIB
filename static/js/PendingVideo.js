document.addEventListener('DOMContentLoaded', function () {
    let listVideo = document.querySelectorAll('.video-list .vid');
    let mainVideo = document.querySelector('.main-video video');
    let title = document.querySelector('.main-video .title');
    let approveButton = document.querySelector('.main-video .approve-btn');
    let editButton = document.querySelector('.main-video .edit-btn');
    let regenerateButton = document.querySelector('.main-video .regenerate-btn');

    function setActiveVideo(video) {
        listVideo.forEach(vid => vid.classList.remove('active'));
        video.classList.add('active');

        if (video.classList.contains('active')) {
            let src = video.querySelector('video').getAttribute('src');
            mainVideo.src = src;
            let text = video.querySelector('.title').innerHTML;
            title.innerHTML = text;
        }
    }

    function approveVideo() {
        let selectedVideo = document.querySelector('.video-list .vid.active');
        if (selectedVideo) {
            // Implement your approve functionality here
            console.log('Video Approved:', selectedVideo.querySelector('.title').innerHTML);
        }
    }

    function editVideo() {
        let selectedVideo = document.querySelector('.video-list .vid.active');
        if (selectedVideo) {
            // Implement your edit functionality here
            console.log('Editing Video:', selectedVideo.querySelector('.title').innerHTML);
        }
    }

    function regenerateVideo() {
        let selectedVideo = document.querySelector('.video-list .vid.active');
        if (selectedVideo) {
            // Implement your regenerate functionality here
            console.log('Regenerating Video:', selectedVideo.querySelector('.title').innerHTML);
        }
    }

    listVideo.forEach(video => {
        video.addEventListener('click', function () {
            setActiveVideo(video);
        });
    });

    approveButton.addEventListener('click', approveVideo);
    editButton.addEventListener('click', editVideo);
    regenerateButton.addEventListener('click', regenerateVideo);
});
