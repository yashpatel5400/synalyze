let shouldStop = false;
let stopped = false;
mediaRecorder = null;
var socket = io.connect('http://' + document.domain + ':' + location.port);

const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');

stopButton.addEventListener('click', function() {
shouldStop = true;
mediaRecorder.stop();
})

var handleSuccess = function(stream) {
  const options = {mimeType: 'video/webm;codecs=vp9'};
  const recordedChunks = [];
  mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) {
      recordedChunks.push(e.data);
    }
  });

  mediaRecorder.addEventListener('stop', function() {
    socket.emit('process', {data: new Blob(recordedChunks)});
  });

  mediaRecorder.start();
};

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
.then(handleSuccess);
