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

connectBtn.addEventListener('click', startCamera);

window.addEventListener('beforeunload', () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
});