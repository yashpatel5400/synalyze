let shouldStop = false;
let stopped = false;
mediaRecorder = null;
var socket = io.connect('https://' + document.domain + ':' + location.port);

function dec2hex (dec) {
  return ('0' + dec.toString(16)).substr(-2)
}

function generateId (len) {
  var arr = new Uint8Array((len || 40) / 2)
  window.crypto.getRandomValues(arr)
  return Array.from(arr, dec2hex).join('')
}

var name = generateId()

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
    socket.emit('process', {
      data: new Blob(recordedChunks),
      filename: name
    });
  });

  mediaRecorder.start();
};

socket.on('completedwrite', function() {
  window.location.href = '../report/' + name;
});


navigator.mediaDevices.getUserMedia({ audio: true, video: false })
.then(handleSuccess);
