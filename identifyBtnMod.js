
/*

Modifications to identify button to capture image of plant and send to model for eval.

- When the Identify button is clicked:
- Captures a snapshot from the live video.
- Converts the frame into a JPEG Blob.
- Sends the image to Roboflow API.
- Receives and displays the detection results.


*/


identifyBtn.addEventListener("click", async () => {
    if (!stream) {
      alert("Please connect to the camera first.");
      return;
    }
  
    // Capture frame from video
    const context = canvasElement.getContext("2d");
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
  
    // Convert to Blob
    canvasElement.toBlob(async (blob) => {
      if (!blob) {
        console.error("Failed to capture image.");
        return;
      }
  
      // Prepare form data for Roboflow API
      const formData = new FormData();
      formData.append("file", blob);
  
      try {
        plantInfo.innerHTML = "<p>Analyzing image...</p>";
  
        // Send image to Roboflow API
        const response = await axios({
          method: "POST",
          url: "https://detect.roboflow.com/tomato-identification/1",
          params: { api_key: "N0pjrXKm1PYOXX2B5jLW" },
          data: formData
        });
  
        // Process response
        if (response.data && response.data.predictions.length > 0) {
          const bestMatch = response.data.predictions[0];
  
          const detectedPlant = {
            name: bestMatch.class || "Unknown Plant",
            confidence: bestMatch.confidence,
            care_tips: [
              "Water regularly but avoid overwatering",
              "Provide adequate sunlight",
              "Use organic fertilizers"
            ] // Customize this dynamically if needed
          };
  
          displayPlantInfo(detectedPlant);
        } else {
          plantInfo.innerHTML = "<p>No plant detected. Try again.</p>";
        }
      } catch (error) {
        console.error("Error detecting plant:", error);
        plantInfo.innerHTML = "<p>Identification failed. Check console for details.</p>";
      }
    }, "image/jpeg");
  });
