const mic_btn = document.querySelector("#mic");
const playback = document.querySelector('.playback');
const interviewer = document.getElementById('interviewer');
const upload = document.getElementById('upload');

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

    var x = new XMLHttpRequest();
    x.open('POST', 'http://127.0.0.1:5000/save');
    x.send(formData); 
    x.onload = function() {
        if (x.status == 200) {
            fetchAudiofromFlask();
        }
    }; 
}

async function fetchAudiofromFlask(){
    try{
        const response = await fetch('http://127.0.0.1:5000/audioFile');

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Convert the response to blob
        const blob = await response.blob();

        // Create a blob URL for the PDF
        const audioURL = window.URL.createObjectURL(blob);
        var audio = new Audio(audioURL);
        audio.play();
        interviewer.play();
        audio.onended = function () {
            interviewer.pause();
        };
    } catch (error) {
        console.error('Error fetching Audio:', error);
    }
}

upload.addEventListener('click', (e)=>{
    e.preventDefault();
    var file = document.getElementById('pdfFile').files[0];
    document.querySelector(".loader").style.display = "block";
    document.querySelector(".back-button").style.display = "none";
    document.querySelector(".profile__container").style.display = "none";
    chrome.runtime.sendMessage("currTab", (response) => {
        var form = new FormData();
        form.append('file', file);
        form.append('text1', response);
        form.append('text2', upload.value);

        var x = new XMLHttpRequest();
        x.open('POST', 'http://127.0.0.1:5000/resume');
        x.send(form); 
        x.onload = function() {
            if (x.status == 200) {
                fetchPdfFromFlask();  
                document.querySelector(".back-button").style.display = "block";
                document.querySelector(".profile__container").style.display = "flex";
                document.querySelector(".loader").style.display = "none";
                alert('Successfully uploaded')
            } else {
                alert("Error Uploading")
            }
        };
    });
    
});

async function fetchPdfFromFlask(){
    try{
        const response = await fetch('http://127.0.0.1:5000/resumeFile');

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Convert the response to blob
        const blob = await response.blob();

        // Create a blob URL for the PDF
        const blobUrl = URL.createObjectURL(blob);

        // Create a link to download the PDF
        const downloadLink = document.createElement('a');

        downloadLink.href = blobUrl;
        downloadLink.download = 'sample.pdf';
        downloadLink.textContent = 'Download PDF';

        // Append the link to the document body and trigger download
        document.body.appendChild(downloadLink);
        downloadLink.click();

        // Clean up
        document.body.removeChild(downloadLink);
        return;
    } catch (error) {
        console.error('Error fetching PDF:', error);
        return;
    }
}