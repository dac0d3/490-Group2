const plantInfo = document.getElementById('plantInfo');
const connectBtn = document.getElementById('connectBtn');
const identifyBtn = document.getElementById('identifyBtn');
const plantStream = document.getElementById('plantStream');
let connected = 0;

//connectBtn.addEventListener('click', startCamera);

//window.addEventListener('beforeunload', () => {
//  if (stream) {
//    stream.getTracks().forEach(track => track.stop());
//  }
//});

//
//function displayPlantInfo(data) {
//  const infoHTML = `
//    <h3>${data.name}</h3>
//    <p>Confidence: ${data.confidence}%</p>
//    <h4>Care Tips:</h4>
//    <ul>
//      ${data.care_tips.map(tip => `<li>${tip}</li>`).join('')}
//    </ul>
//  `;
//  plantInfo.innerHTML = infoHTML;
//}


identifyBtn.addEventListener('click', displayPlantInfo);
async function displayPlantInfo() {
    if (connected > 0) {
        output = "<p>No plants detected in image</p>"
        responses = await fetch('/data_feed').then(res => res.json());
        if (responses.length > 0) {
            output = ""
            for (i = 0; i < responses.length; i++) {
                output += "<p>Detected " + responses[i].name + " at coordinates x:" + ((responses[i].box.x1 + responses[i].box.x2)/2) + ", y: " + ((responses[i].box.y1 + responses[i].box.y2)/2) +"</p>";
            }
        }
        plantInfo.innerHTML = output
    }
    else {
        plantInfo.innerHTML = "<p>No camera connected! Please initialize camera first</p>"
    }
}

connectBtn.addEventListener('click', showPlantDisplay);
async function showPlantDisplay() {
    connected = 1;
    html = `hi`
    plantStream.innerHTML = "<img src='/prediction_feed' /> <div class='stream-status'>Live Feed</div>"
    connectBtn.style.backgroundColor = '#45a049';
    connectBtn.textContent = 'Connected';
}