Below is an example of a comprehensive `README.md` file that documents both code files. You can adjust the file names, installation instructions, and other details as needed.

---

```markdown
# Scan to PDF Utility for Epson XP-4100 Series

This repository contains two tools for scanning documents with an Epson XP-4100 Series scanner using the airscan interface. The scanned document is first saved as a TIFF image and then converted to a PDF file using ImageMagick.

There are two implementations:

- **Python GUI Application:** A PyQt6-based graphical user interface with a modern QDarkStyle theme.
- **Bash Script:** A command-line tool for scanning and converting documents.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Python GUI Application](#python-gui-application)
  - [Bash Script](#bash-script)
- [Usage](#usage)
  - [Running the Python GUI Application](#running-the-python-gui-application)
  - [Running the Bash Script](#running-the-bash-script)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Dual Interface:** Choose between a user-friendly GUI or a straightforward command-line script.
- **Scan & Convert:** The tools use `scanimage` to perform the scan and ImageMagick's `convert` to generate a PDF.
- **Customizable Options:** Set filenames for both TIFF and PDF outputs and select scanning modes (Color, Gray, or Lineart).

## Requirements

- **Hardware:** Epson XP-4100 Series scanner (or compatible device using airscan).
- **Software:**
  - [`scanimage`](http://www.sane-project.org/) – Part of the SANE project.
  - [ImageMagick](https://imagemagick.org/) – Specifically, the `convert` utility.
- **Python Dependencies (for the GUI):**
  - Python 3.x
  - [PyQt6](https://pypi.org/project/PyQt6/)
  - [QDarkStyle](https://pypi.org/project/qdarkstyle/)

## Installation

### Python GUI Application

1. **Install Python Packages:**

   Make sure you have Python 3 installed, then run:

   ```bash
   pip install PyQt6 qdarkstyle
   ```

2. **Verify External Tools:**

   Ensure that `scanimage` and ImageMagick's `convert` are installed and available in your system's PATH.

### Bash Script

1. **Ensure Prerequisites:**

   Verify that your system has a Bash shell and that both `scanimage` and `convert` are installed.

2. **Make the Script Executable:**

   ```bash
   chmod +x scan_to_pdf.sh
   ```

## Usage

### Running the Python GUI Application

1. **Launch the Application:**

   ```bash
   python scan_to_pdf_gui.py
   ```

2. **Interact with the GUI:**

   - Enter the desired filenames for the TIFF and PDF.
   - Select the scanning mode (Color, Gray, or Lineart).
   - Click the **Scan & Convert** button to start scanning and conversion.
   - A success message will appear once the PDF is generated.

### Running the Bash Script

1. **Execute the Script:**

   ```bash
   ./scan_to_pdf.sh
   ```

2. **Follow the Prompts:**

   - Enter the output TIFF filename.
   - Enter the final PDF filename.
   - Choose the scanning mode by entering 1 (Color), 2 (Gray), or 3 (Lineart).
   - The script will scan and then convert the TIFF to a PDF.

## Code Files

### Python GUI Application (`scan_to_pdf_gui.py`)

```python
import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt
import qdarkstyle

class ScanToPdfGUI_QDark(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan to PDF - Epson XP-4100 (QDarkStyle)")
        self.setMinimumSize(400, 250)

        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # TIFF filename label & input
        self.tiff_label = QLabel("TIFF file name:")
        self.tiff_input = QLineEdit("scanned_output.tiff")

        # PDF filename label & input
        self.pdf_label = QLabel("PDF file name:")
        self.pdf_input = QLineEdit("scanned_output.pdf")

        # Scan mode label & dropdown
        self.mode_label = QLabel("Scanning mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Color", "Gray", "Lineart"])

        # Button to start scanning
        self.scan_button = QPushButton("Scan & Convert")
        self.scan_button.clicked.connect(self.scan_and_convert)

        # Add widgets to the layout
        layout.addWidget(self.tiff_label)
        layout.addWidget(self.tiff_input)
        layout.addWidget(self.pdf_label)
        layout.addWidget(self.pdf_input)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combo)
        layout.addWidget(self.scan_button)

    def scan_and_convert(self):
        tiff_file = self.tiff_input.text().strip()
        pdf_file = self.pdf_input.text().strip()
        scan_mode = self.mode_combo.currentText()

        if not tiff_file or not pdf_file:
            QMessageBox.warning(self, "Warning", "Please specify both TIFF and PDF filenames.")
            return

        try:
            # 1) Run scanimage to produce the TIFF
            with open(tiff_file, "wb") as tiff_output:
                subprocess.run([
                    "scanimage",
                    "--device", "airscan:e0:EPSON XP-4100 Series",
                    "--resolution", "300",
                    "--mode", scan_mode,
                    "--format", "tiff"
                ],
                    check=True,
                    stdout=tiff_output  # Save output as a TIFF file
                )

            # 2) Convert TIFF to PDF using ImageMagick's convert
            subprocess.run([
                "convert",
                tiff_file,
                pdf_file
            ], check=True)

            # Success message
            QMessageBox.information(self, "Success", f"Done! Your PDF has been saved as: {pdf_file}")

        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "Could not find a required command (scanimage or convert). Please ensure they are installed."
            )
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"An error occurred while running a command:\n{e}")

def main():
    app = QApplication(sys.argv)
    # Apply QDarkStyleSheet
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))

    window = ScanToPdfGUI_QDark()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Bash Script (`scan_to_pdf.sh`)

```bash
#!/usr/bin/env bash
#
# scan_to_pdf.sh
# A script to scan from an Epson XP-4100 Series device using airscan,
# then convert the TIFF output to PDF using ImageMagick.

# Prompt for the output TIFF filename
read -p "Enter the output TIFF filename (e.g., scanned_output.tiff): " TIFF_FILE

# Prompt for the final PDF filename
read -p "Enter the final PDF filename (e.g., scanned_output.pdf): " PDF_FILE

# Offer a choice of scan modes
echo "Choose a scanning mode:"
echo "  1) Color"
echo "  2) Gray"
echo "  3) Lineart"
read -p "Enter your choice (1/2/3): " MODE_CHOICE

# Set the scan mode based on the user's choice
case "$MODE_CHOICE" in
  1)
    SCAN_MODE="Color"
    ;;
  2)
    SCAN_MODE="Gray"
    ;;
  3)
    SCAN_MODE="Lineart"
    ;;
  *)
    echo "Invalid choice. Defaulting to Color."
    SCAN_MODE="Color"
    ;;
esac

# Perform the scan using scanimage
echo "Scanning in $SCAN_MODE mode; saving to $TIFF_FILE ..."
scanimage \
  --device "airscan:e0:EPSON XP-4100 Series" \
  --resolution 300 \
  --mode "$SCAN_MODE" \
  --format=tiff > "$TIFF_FILE"

# Check if the scan was successful
if [[ $? -ne 0 ]]; then
  echo "Error: scanimage failed."
  exit 1
fi

# Convert the TIFF to PDF using ImageMagick's 'convert'
echo "Converting $TIFF_FILE to PDF -> $PDF_FILE ..."
convert "$TIFF_FILE" "$PDF_FILE"

if [[ $? -ne 0 ]]; then
  echo "Error: failed to convert TIFF to PDF."
  exit 1
fi

echo "Done! Your PDF is saved as: $PDF_FILE"
```

## Troubleshooting

- **Command Not Found:**  
  If you see errors related to missing commands, verify that both `scanimage` and ImageMagick’s `convert` are installed and available in your PATH.

- **Python Errors:**  
  For the GUI application, ensure that PyQt6 and qdarkstyle are correctly installed via pip.

- **Permission Issues:**  
  If you encounter permission issues, you might need to run the script with elevated privileges (e.g., using `sudo`).

## License

This project is licensed under the [MIT License](LICENSE).
