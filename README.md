# Image Steganography Using LSB Technique

A simple Python-based steganography project that hides a secret message and passcode in an image using the Least-Significant-Bit (LSB) encoding technique, allowing secure retrieval of the message later.

## Overview

This project employs robust LSB steganography to embed a secret message along with a passcode into an image. It consists of a Python backend and an HTML frontend for ease of use.

## Features

### Encryption:

- Embeds a secret message and passcode into `mypic.jpg`.
- Saves the resulting image as `encrypted.png`.

### Decryption:

- Retrieves the hidden message from `encrypted.png`.
- Requires the correct passcode for extraction.

### User-Friendly Interface:

- Provides an intuitive frontend built using HTML, CSS, and JavaScript.
- Communicates with the backend via API calls.

### Robust Data Storage:

- Uses a header to store the lengths of the passcode and message for accurate extraction.

## Requirements

- Python 3.x
- Flask
- OpenCV
- NumPy

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Manasa120205/Image-Steganography.git
   cd Secure-Image-Steganography
   ```
2. Install the required libraries:
   ```sh
   pip install flask opencv-python numpy
   ```
3. Place an image named `mypic.jpg` in the project directory.

## Usage

### Running the Backend

```sh
python app.py
```

This starts the Flask server to handle encryption and decryption requests.

### Running the Frontend

Open `index.html` in a web browser to use the GUI.

## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed modifications.

## Author

GitHub:   (https://github.com/Manasa120205/Image-Steganography.git)
