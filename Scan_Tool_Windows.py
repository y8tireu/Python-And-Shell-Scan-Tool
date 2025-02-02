import sys
import subprocess
import platform
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
            if platform.system() == "Windows":
                # On Windows, use WIA via pywin32 to scan
                self.scan_with_wia(tiff_file, scan_mode)
            else:
                # On Linux/macOS, use the command-line scanimage tool.
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

            # Convert TIFF to PDF using ImageMagick.
            if platform.system() == "Windows":
                # Use the 'magick' command to avoid conflict with Windows' built-in convert.
                subprocess.run([
                    "magick", "convert", tiff_file, pdf_file
                ], check=True)
            else:
                subprocess.run([
                    "convert", tiff_file, pdf_file
                ], check=True)

            # Success message
            QMessageBox.information(self, "Success", f"Done! Your PDF has been saved as: {pdf_file}")

        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "Could not find a required command (scanimage/magick or convert). Please ensure they are installed."
            )
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"An error occurred while running a command:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def scan_with_wia(self, filename, scan_mode):
        """
        Uses Windows Image Acquisition (WIA) via pywin32 to perform a scan and save the result as a TIFF file.
        """
        try:
            import win32com.client
        except ImportError:
            raise Exception("pywin32 is not installed. Please install it to enable scanning on Windows.")

        commonDialog = win32com.client.Dispatch("WIA.CommonDialog")
        # Map scan_mode to WIA image intent:
        # ColorIntent = 1, GrayscaleIntent = 2, TextIntent (lineart) = 4.
        intent_mapping = {"Color": 1, "Gray": 2, "Lineart": 4}
        intent = intent_mapping.get(scan_mode, 1)
        # TIFF format GUID for WIA:
        tiff_format = "{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}"
        # ShowAcquireImage parameters:
        #   DeviceType: 1 (Scanner)
        #   Intent: as mapped above
        #   Bias: 0 (default)
        #   FormatID: TIFF format GUID
        #   AlwaysSelectDevice: True (forces the selection dialog, in case multiple devices are present)
        image = commonDialog.ShowAcquireImage(1, intent, 0, tiff_format, True)
        if image is None:
            raise Exception("No image was acquired from the scanner.")
        image.SaveFile(filename)

def main():
    app = QApplication(sys.argv)
    # Apply QDarkStyleSheet
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))

    window = ScanToPdfGUI_QDark()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
