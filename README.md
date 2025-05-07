# FloraSight
 
Requirements are listed in `requirements.txt`. Install using `pip install -r requirements.txt` in your venv before running.
If you wish to utilize CUDA acceleration, please install the CUDA version of PyTorch found [here](https://pytorch.org/get-started/locally/).

Start program via the command:
```python main.py```

The webui IP will default to 127.0.0.1:5000

## Deployment Documentation
### Server Requirements:
- Python 3.9 or later installed
- CUDA supported GPU required for CUDA acceleration. List is available [here](https://developer.nvidia.com/cuda-gpus)
  - This is not necessarily required, but heavily reccommended.
- OS Support:
  - Windows: 7+
  - Linux: Any distribution which utilize [glibc](https://www.gnu.org/software/libc/) >= 2.17 (This should include the majority of modern Linux distributions)
  - Macintosh: macOS 10.15+
    - CUDA is unsupported on macOS, and as such software performance will be significantly degraded, and is therefore not recommended

 ### Client Requirements:
- Camera accessible to web browser
- Modern web browser capable of parsing JavaScript and displaying images

## User Manual
### Standard Usage:
Basic usage of the FloraSight system is fairly straightforward:
1. With a command prompt open to the root folder of the program, initialize the server as stated above with the command `python main.py`
2. Once the server has been initialized, navigate to the webui located at the default IP address of 127.0.0.1:5000
3. Before object detection can occur, the connected camera must be initialized by clicking the "Connect" button on the left side of the screen
4. Once the camera has been initialized, object detection will occur continuously in real-time so long as the video feed is still available
5. After this point:
    * At any time, the "Identify" button on the left side of the screen may be clicked to manually print out the results of the detection, including both classes and coordinates
    * Additionally, this same data can be access from the `/data_feed` api endpoint as an array of JSON objects, and can be used in a variety of ways at the user's discretion

### Troubleshooting:
- The camera framerate is extremely low
  - Ensure that the server computer has a CUDA compatible GPU as outlined in the system requirements
  - Ensure that the CUDA enabled versions of the torch, torchvision, and torchaudio libraries are installed, as outlined in the installation instructions
- The camera feed isn't visible
  - Ensure that a camera is physically connected to the client computer
  - Ensure that your web browser has permission to access your camera
- The `/data_feed` API just displays an empty `[]`
  - If the FloraSight system doesn't detect any objects, it will return nothing, represented by the empty array `[]`
- The server doesn't initialize properly
  - Make sure that during installation of PyTorch, all components were successfuly installed
  - Make sure that your system meets the minimum requirements as outlined above
  - Uninstall and reinstall all Python libraries
