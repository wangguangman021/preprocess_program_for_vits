document.getElementById('audio-form').addEventListener('submit', function(event) {  
  event.preventDefault(); // 阻止表单默认的提交行为  
  
  var language = document.getElementById('language').value;  
  var whisperSize = document.getElementById('whisper-size').value;  
  var audioFile = document.getElementById('audio-file').files[0];  
  
  if (audioFile) {  
    var formData = new FormData();  
    formData.append('audio-file', audioFile);  
    formData.append('language', language);  
    formData.append('whisper-size', whisperSize);  
  
    fetch('http://localhost:8080/api', {  
      method: 'POST',  
      body: formData,  
    })  
    .then(response => response.text())  
    .then(data => {  
      document.getElementById('result').innerText = data;  
    })  
    .catch(error => {  
      console.error('Error:', error);  
    });  
  } else {  
    alert('Please select an audio file.');  
  }  
});