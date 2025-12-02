# Sahel Font - Development Repository

A Persian (Farsi) font with variable version support. This repository contains the source files and build tools for developing and building the Sahel font family.

![Sahel Variable Font Demo](./sample-variable.gif)

## 🚀 Features

- **Multiple weights**: Light (300), Regular (400), SemiBold (600), Bold (700), Black (900)
- **Variable font**: Single file with adjustable weight axis
- **Multiple formats**: TTF, WOFF, WOFF2, EOT
- **Persian/Farsi support**: Optimized for Persian typography
- **Web-ready**: Includes CSS font-face declarations

## 📋 Prerequisites

To build the fonts from source, you'll need:

- **FontForge**: Font editor and converter
- **Python 3**: For build scripts
- **fontmake**: Python tool for building fonts
- **woff2_compress**: Tool for creating WOFF2 files

### Installing Dependencies

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y fontforge python3 python3-pip
pip3 install fontmake
sudo apt-get install -y woff2
```

#### macOS

```bash
brew install fontforge python3
pip3 install fontmake
brew install woff2
```

#### Arch Linux

```bash
sudo pacman -S fontforge python python-pip woff2
pip install fontmake
```

## 🔨 Building the Fonts

### Building Variable Font

To build the variable font from source files:

```bash
cd variable
./makevariable.sh ../dist
```

This will:
1. Convert SFD source files to UFO format
2. Fix feature definitions
3. Generate variable TTF font
4. Compress to WOFF2 format
5. Clean up temporary files

### Building Static Fonts

The static font files (TTF, WOFF, WOFF2, EOT) for each weight are pre-built and available in the `dist/` directory. To rebuild them, you would need the fontbuilder tool (see original repository).

## 📁 Repository Structure

```
sahel-font/
├── source/          # Source SFD (FontForge) files
│   ├── Sahel.sfd
│   ├── Sahel-Bold.sfd
│   ├── Sahel-Black.sfd
│   ├── Sahel-SemiBold.sfd
│   └── Sahel-Light.sfd
├── variable/        # Variable font build scripts
│   ├── makevariable.sh       # Main build script
│   ├── fix-features-fea.py   # Feature file fixer
│   ├── fontforge.pe          # FontForge script
│   └── Sahel.designspace     # Designspace file
├── dist/            # Built font files
│   ├── Sahel*.ttf
│   ├── Sahel*.woff
│   ├── Sahel*.woff2
│   ├── Sahel*.eot
│   ├── Sahel-VF.ttf          # Variable font
│   ├── Sahel-VF.woff2        # Variable font (compressed)
│   └── font-face.css         # CSS declarations
└── build.conf       # Build configuration
```

## 🧪 Testing

After building, you can test the fonts by:

1. Installing them on your system
2. Opening them in FontForge to inspect
3. Using the web font-face declarations in a test HTML page

## 🤝 Contributing

This is a fork of the original [Sahel Font](https://github.com/rastikerdar/sahel-font) repository. 

### Development Workflow

1. Modify source files in `source/` directory using FontForge
2. Build the variable font using the scripts in `variable/`
3. Test the built fonts
4. Commit your changes

### Code Style

- Shell scripts: Use clear variable names, add comments for complex operations
- Python scripts: Follow PEP 8 guidelines
- Add helpful console output with colors and emojis

## 📦 Continuous Integration

This repository includes GitHub Actions workflows for automated building and testing:

- **Build**: Automatically builds fonts on push and pull requests
- **Release**: Creates releases with built font artifacts
- **Artifact Upload**: Uploads built fonts as GitHub Actions artifacts

## 🐛 Known Issues

### Variable Font Issues
- Mark placement distortion in some contexts

## 📝 To-Do List

- [ ] Font testing page
- [ ] Add Latin characters from an open-source variable font
- [ ] Test font in all supported applications
- [ ] Add additional variable font axes (e.g., width, slant)

## 📄 License

This project is licensed under the SIL Open Font License (OFL). See the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Original Author**: Saber Rastikerdar ([@rastikerdar](https://github.com/rastikerdar))
- **Contributors**: Amin Abedi ([@aminabedi68](https://github.com/aminabedi68))
- **Tools**: Built with [FontForge](https://fontforge.github.io)

## 📚 Resources

- [Original Sahel Font Repository](https://github.com/rastikerdar/sahel-font)
- [Font Preview](http://rastikerdar.github.io/sahel-font/)
- [FontForge Documentation](https://fontforge.org/docs/)
- [Variable Fonts Guide](https://web.dev/variable-fonts/)
