const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const resultDiv = document.getElementById('result');
const img = document.getElementById('img');
let stream;
 
var width = 360;
var height = 540;

const constraints = {
    width: 240,
    height: 320,
}
const Styles = {
    Video: { width: "100%", height: "100%", background: 'rgba(245, 240, 215, 0.5)' },
    None: { display: 'none' },
  }

navigator.mediaDevices.getUserMedia({ audio: false, video: constraints })
    .then(streamObj => {
        stream = streamObj;
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        tick(video);
    })
    .catch(err => console.error(err));

function tick(video) {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        var imgUrl = '';

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code || imgUrl !== '') {
            console.log('Decoded Data:', code.data);

            // 포토이즘
            if (true) {
                const hostname = new URL(code.data).hostname;
                const urlParams = new URLSearchParams(new URL(code.data).search);
                const id = urlParams.get('id');

                console.log('url :', code.data);
                console.log('host :', hostname);
                console.log('id :', id);

                imgUrl = `http://${hostname}/take/${id}.jpg`;
            }
            console.log('str :', imgUrl);

            stream.getTracks().forEach(track => track.stop()); // 카메라 스트림 중지
            canvas.style.display = 'none';
            resultDiv.innerHTML = `사진 URL: ${imgUrl}<br><a href="${imgUrl}" target="_blank"><img src="${imgUrl}" width="100%"></a>`;
        }
    }
    requestAnimationFrame(() => tick(video));
}
