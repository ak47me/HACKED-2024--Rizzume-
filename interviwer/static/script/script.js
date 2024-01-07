const mic_btn = document.querySelector("#mic");
const playback = document.querySelector('.playback');
const interviewer = document.getElementById('interviewer');

mic_btn.addEventListener('click', ToggleMic);

let can_record = false;
let is_recording = false;

let recorder = null;

let chunks = []

function SetupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({
                audio: true
            })
            .then(SetupStream)
            .catch(err => {
                console.error(err)
            });
    }
}

SetupAudio();

function SetupStream(stream) {
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => {
        chunks.push(e.data);
    }

    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;

        saveAudio(blob);


    }

    can_record = true;
}

function ToggleMic() {
    if (!can_record) return;

    is_recording = !is_recording;

    if (is_recording) {
        recorder.start();
        // pause the video
        interviewer.pause();
        mic_btn.classList.add("is-recording");
    } else {
        recorder.stop();
        mic_btn.classList.remove("is-recording");
    }
}

function saveAudio(blob) {
    let formData = new FormData();
    formData.append('file', blob, 'recorded_audio.mp3');
    console.log(formData);
    fetch('/save', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
        .then(blob => {
            const audioURL = window.URL.createObjectURL(blob);
            var audio = new Audio(audioURL);
            audio.play();
            interviewer.play();
            audio.onended = function () {
                interviewer.pause();
            };
        })
        .catch(err => {
            console.error(err);
        });

};



