# scan_to_pdf.sh

A simple Bash script to scan from an Epson XP-4100 Series device using `airscan`,
then convert the TIFF output to PDF using ImageMagick.

## Requirements
- [scanimage](http://www.sane-project.org/)
- [ImageMagick](https://imagemagick.org/)
- Epson XP-4100 Series device accessible via airscan

## Usage

1. **Make the script executable** (once you save it to a file, e.g., `scan_to_pdf.sh`):
   ```bash
   chmod +x scan_to_pdf.sh
   ```
2. **Run the script**:
   ```bash
   ./scan_to_pdf.sh
   ```
3. **Follow the prompts** to:
   - Enter a TIFF filename
   - Enter a PDF filename
   - Choose a scanning mode (Color, Gray, or Lineart)

## Script

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

