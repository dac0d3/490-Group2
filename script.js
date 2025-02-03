// Global variables
let stream = null;

// DOM elements
const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const plantInfo = document.getElementById('plantInfo');

// Button elements
const connectBtn = document.getElementById('connectBtn');
const identifyBtn = document.getElementById('identifyBtn');

// Helper function to see if we can safely call getUserMedia
function hasModernGetUserMedia() {
  return (
    navigator.mediaDevices &&
    typeof navigator.mediaDevices.getUserMedia === 'function'
  );
}

// Fallback support for older browsers
function getLegacyUserMedia(constraints) {
  // Try to assign vendor-prefixed getUserMedia
  const getUserMedia = navigator.getUserMedia
    || navigator.webkitGetUserMedia
    || navigator.mozGetUserMedia
    || navigator.msGetUserMedia;

  if (!getUserMedia) return null;

  // Return a Promise-like wrapper for older getUserMedia
  return new Promise((resolve, reject) => {
    getUserMedia.call(navigator, constraints, resolve, reject);
  });
}

// 1. Camera Initialization with Fallback
async function startCamera() {
  // Step 1: Check for getUserMedia support
  if (!hasModernGetUserMedia()) {
    // Attempt fallback approach
    const fallback = getLegacyUserMedia({ video: true, audio: false });
    if (!fallback) {
      alert("Browser does not support camera API. Please use a modern browser (or update iOS).");
      return;
    }
    try {
      stream = await fallback;
    } catch (legacyErr) {
      console.error("Legacy getUserMedia failed:", legacyErr);
      alert("Unable to access camera. Check permissions or update your browser.");
      return;
    }
  } else {
    // We have modern getUserMedia
    // Attempt environment-facing camera first
    const environmentConstraints = {
      video: { facingMode: { exact: "environment" } },
      audio: false
    };
    try {
      stream = await navigator.mediaDevices.getUserMedia(environmentConstraints);
      console.log("Environment camera obtained.");
    } catch (envError) {
      console.warn("Environment camera not found or not accessible:", envError);

      // Fallback to any available camera (e.g., front camera)
      const fallbackConstraints = { video: true, audio: false };
      try {
        stream = await navigator.mediaDevices.getUserMedia(fallbackConstraints);
        console.log("Fallback to default camera succeeded.");
      } catch (fallbackError) {
        console.error("No camera could be accessed:", fallbackError);
        alert(`Unable to access camera: ${fallbackError.message}`);
        return;
      }
    }
  }

  // If we have a valid stream
  if (stream) {
    videoElement.srcObject = stream;
    connectBtn.style.backgroundColor = '#45a049';
    connectBtn.textContent = 'Connected';
  }
}

// 2. Identify Button Functionality
identifyBtn.addEventListener('click', async () => {
  if (!stream) {
    alert('Please connect to the camera first');
    return;
  }

  const context = canvasElement.getContext('2d');
  canvasElement.width = videoElement.videoWidth;
  canvasElement.height = videoElement.videoHeight;
  context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

  const imageData = canvasElement.toDataURL('image/jpeg');
  identifyPlant(imageData);
});

// 3. Pseudo Function for Plant Identification
async function identifyPlant(imageData) {
  plantInfo.innerHTML = '<p>Analyzing image...</p>';

  // Simulate a 2 second "analysis" delay
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const mockResponse = {
    name: 'Tomato (Tomate)',
    confidence: 0.92,
    care_tips: [
      'Moderate indirect light',
      'Water when top soil is dry',
      'Prefers humid environment'
    ]
  };

  displayPlantInfo(mockResponse);
}

// 4. Display Plant Information
function displayPlantInfo(data) {cam
  const infoHTML = `
    <h3>${data.name}</h3>
    <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
    <h4>Care Tips:</h4>
    <ul>
      ${data.care_tips.map((tip) => `<li>${tip}</li>`).join('')}
    </ul>
  `;
  plantInfo.innerHTML = infoHTML;
}

// 5. Connect Button Event
connectBtn.addEventListener('click', startCamera);

// 6. Stop Camera Stream on Page Unload
window.addEventListener('beforeunload', () => {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
});
