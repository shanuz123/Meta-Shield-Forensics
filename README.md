<div align="center">

  <img src="https://img.icons8.com/fluency/96/000000/fingerprint-scan.png" alt="logo" width="100" height="100" />

  <h1>🛡️ Meta-Shield Forensics</h1>
  
  <p>
    <b>The Ultimate Privacy & Metadata Sanitization Tool</b>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Cybersecurity-Forensics-red?style=for-the-badge&logo=kali-linux&logoColor=white" alt="Security" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
  </p>

  <br />

</div>

---

**Meta-Shield** is a Python-based privacy tool designed to inspect and "clean" metadata (EXIF) from digital images. It features a modern, dark-mode GUI and powerful forensic capabilities to help users understand what data is hidden in their photos before sharing them online.

## Features
*   **Drag & Drop Loading**: Easily select images to inspect.
*   **Forensic Inspector**: improved detection logic that reveals:
    *   Camera Make/Model
    *   Date & Time Original
    *   Software Used
    *   **GPS Coordinates** (with automatic link to Google Maps)
*   **Privacy scrubbing**: Strips *all* metadata tags and saves a clean copy (`filename_clean.jpg`).
*   **Diganostic Mode**: Smartly detects if GPS data was stripped by other apps (like Snapseed or WhatsApp) while other metadata remains.
*   **Modern UI**: Built with `customtkinter` for a sleek dark mode appearance.

## Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/shanuz123/Meta-Shield-Forensics.git
    cd meta-shield
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1.  Run the application:
    ```bash
    python meta_shield.py
    ```
2.  Click **Select Image** to load a JPEG/TIFF file.
3.  Review the **Metadata Inspector** panel on the right.
4.  Click **REMOVE METADATA & SAVE** to create a privacy-safe copy of your image.

## Requirements
*   Python 3.x
*   `customtkinter`
*   `Pillow`

## License
MIT License.
