# Flask Object Detection
 
Requirements are listed in `requirements.txt`. Install using `pip install -r requirements.txt` in your venv before running.
If you wish to utilize CUDA acceleration, please install the CUDA version of PyTorch found [here](https://pytorch.org/get-started/locally/).

Start program via the command:
```python main.py```

The webui IP will default to 120.0.0.1:5000

## Server Requirements:
- Python 3.9 or later installed
- CUDA supported GPU required for CUDA acceleration. List is available [here](https://developer.nvidia.com/cuda-gpus)
  - This is not necessarily required, but heavily reccommended.
- OS Support:
  - Windows: 7+
  - Linux: Any distribution which utilize [glibc](https://www.gnu.org/software/libc/) >= 2.17 (This should include the majority of modern Linux distributions)
  - Macintosh: macOS 10.15+
    - CUDA is unsupported on macOS, and as such software performance will be significantly degraded, and is therefore not recommended

 ## Client Requirements:
- Camera accessible to web browser
- Modern web browser capable of parsing JavaScript and displaying images
