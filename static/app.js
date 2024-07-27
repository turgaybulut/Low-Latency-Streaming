import jsQR from "./jsQR.js";
var url = "http://localhost:8000/ldash/1.mpd";
var player = dashjs.MediaPlayer().create();

player.initialize(document.querySelector("#video-player"), url, false);

document.getElementById("goToLiveButton").onclick = function () {
    player.seek(player.duration());
};

function readQrCode() {
    var video = document.getElementById("video-player");
    var canvas = document.createElement('canvas');
    var qrWidth = video.videoWidth * 0.3;
    var qrHeight = video.videoHeight * 0.3;
    canvas.width = qrWidth;
    canvas.height = qrHeight;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, video.videoWidth - qrWidth, 0, qrWidth, qrHeight, 0, 0, qrWidth, qrHeight);
    var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var code = jsQR(imageData.data, imageData.width, imageData.height);
    if (code) {
        var latency = (Date.now() / 1000) - parseFloat(code.data);
        document.getElementById("latency").innerText = "Latency: " + latency + " seconds";
    }
}

setInterval(readQrCode, 500);