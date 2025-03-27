// ==============================================
// 1. Global Variables
// ==============================================
let stream = null;

const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const plantInfo = document.getElementById('plantInfo');

const connectBtn = document.getElementById('connectBtn');
const identifyBtn = document.getElementById('identifyBtn');

// ==============================================
// 2. Helper Functions for Camera Access
// ==============================================
function hasModernGetUserMedia() {
  return (
    navigator.mediaDevices &&
    typeof navigator.mediaDevices.getUserMedia === 'function'
  );
}

function getLegacyUserMedia(constraints) {
  const getUserMedia =
    navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia;
  if (!getUserMedia) return null;
  return new Promise((resolve, reject) => {
    getUserMedia.call(navigator, constraints, resolve, reject);
  });
}

// ==============================================
// 3. Start Camera
// ==============================================
async function startCamera() {
  if (!hasModernGetUserMedia()) {
    const fallback = getLegacyUserMedia({ video: true, audio: false });
    if (!fallback) {
      alert("Browser does not support camera API. Please use a modern browser.");
      return;
    }
    try {
      stream = await fallback;
    } catch (err) {
      console.error("Legacy getUserMedia failed:", err);
      alert("Unable to access camera. Check permissions.");
      return;
    }
  } else {
    const constraints = { video: true, audio: false };
    try {
      stream = await navigator.mediaDevices.getUserMedia(constraints);
    } catch (err) {
      console.error("Error accessing camera:", err);
      alert("Unable to access camera: " + err.message);
      return;
    }
  }
  
  if (stream) {
    videoElement.srcObject = stream;
    connectBtn.style.backgroundColor = '#45a049';
    connectBtn.textContent = 'Connected';
  }
}

// ==============================================
// 4. Identify Button Functionality
// ==============================================
identifyBtn.addEventListener('click', async () => {
  if (!stream) {
    alert('Please connect to the camera first');
    return;
  }
  
  const context = canvasElement.getContext('2d');
  canvasElement.width = videoElement.videoWidth;
  canvasElement.height = videoElement.videoHeight;
  context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

  canvasElement.toBlob(async (blob) => {
    if (!blob) {
      console.error('Failed to capture image.');
      return;
    }
    identifyPlant(blob);
  }, 'image/jpeg');
});

/**
 * identifyPlant: Sends the captured image to /predict/ via Axios.
 *                Expects a YOLO-style response with "detections".
 */
async function identifyPlant(blob) {
  // 4A) Update the UI to show that we're processing
  plantInfo.innerHTML = '<p>Analyzing image...</p>';
  
  // 4B) Build the form data for POST
  const formData = new FormData();
  formData.append('file', blob, 'capture.jpg');
  
  try {
    // 4C) Make the request to /predict/
    const response = await axios.post('/predict/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // 4D) Check for YOLO-style "detections" array
    if (response.data && Array.isArray(response.data.detections)) {
      const detections = response.data.detections;
      
      if (detections.length > 0) {
        // 4E) For now, just use the first detection
        const firstDet = detections[0];
        
        // 4F) Map the class_id to a human-readable label
        //     If your YOLO model has multiple classes, expand this map:
        const classMap = {
          0: "Tomato",       // example
          1: "Potato",       // example
          // ... add more if needed ...
        };
        
        const classLabel = classMap[firstDet.class_id] || "Unknown";
        const confidence = (firstDet.confidence * 100).toFixed(1);

        // 4G) Build a "plantData" object to pass to displayPlantInfo
        const plantData = {
          name: classLabel,
          confidence: confidence,
          care_tips: [
            "Water regularly but avoid overwatering",
            "Provide adequate sunlight",
            "Use organic fertilizers"
          ]
        };

        // 4H) Display the plant info
        displayPlantInfo(plantData);
      } else {
        // 4I) No detections in the array => handle no plant scenario
        plantInfo.innerHTML = '<p>No plant detected. Try again.</p>';
      }
    } else {
      // 4J) The server responded but didn't provide the expected "detections"
      plantInfo.innerHTML = '<p>No plant detected. Try again.</p>';
    }
  } catch (error) {
    console.error('Error detecting plant:', error);
    plantInfo.innerHTML = '<p>Identification failed. Check console for details.</p>';
  }
}

/**
 * displayPlantInfo: Updates the UI with name, confidence, and care tips.
 *                   (You can customize the HTML layout as you wish.)
 */
function displayPlantInfo(data) {
  const infoHTML = `
    <h3>${data.name}</h3>
    <p>Confidence: ${data.confidence}%</p>
    <h4>Care Tips:</h4>
    <ul>
      ${data.care_tips.map(tip => `<li>${tip}</li>`).join('')}
    </ul>
  `;
  plantInfo.innerHTML = infoHTML;
}

// ==============================================
// 5. Connect Button
// ==============================================
connectBtn.addEventListener('click', startCamera);

// ==============================================
// 6. Cleanup On Unload
// ==============================================
window.addEventListener('beforeunload', () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
});
