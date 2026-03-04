#!/bin/bash
# Downloads required fonts for PYRE into assets/fonts/
# Run once from project root: bash scripts/download_fonts.sh

FONTS_DIR="assets/fonts"
mkdir -p "$FONTS_DIR"

echo "Downloading Anton..."
curl -sL "https://fonts.gstatic.com/s/anton/v25/1Ptgg87LROyAm0K08i4gS7lu.woff2" -o "$FONTS_DIR/Anton-Regular.woff2"
curl -sL "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf" -o "$FONTS_DIR/Anton-Regular.ttf"

echo "Downloading Bebas Neue..."
curl -sL "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf" -o "$FONTS_DIR/BebasNeue-Regular.ttf"

echo "Downloading JetBrains Mono..."
curl -sL "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf" -o "$FONTS_DIR/JetBrainsMono-Regular.ttf"

echo "Downloading Inter..."
curl -sL "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf" -o "$FONTS_DIR/Inter-Variable.ttf"

echo "Done. Fonts saved to $FONTS_DIR/"
