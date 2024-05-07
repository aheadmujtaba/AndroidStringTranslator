# String Translator

This Python script automates the translation of strings in an XML file to multiple languages using Google Translate. It also includes a standalone executable for Windows users.

## Prerequisites

- Python 3.x
- aiohttp library (install using `pip install aiohttp`)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/string-translator.git
```

Navigate to the project directory:

```bash
cd string-translator
```

Install the required Python dependencies:

```bash
pip install aiohttp
```

For Windows users, download the standalone executable `stringtranslator.exe` from the [Releases](https://github.com/your-username/string-translator/releases) section of this repository.

## Usage

### Using Python Script

#### Prerequisites:

- Input XML file with strings to be translated (`strings.xml`)
- Input language code (e.g., `en` for English)
- Output language codes for desired translations

#### Usage:

```bash
python translate_strings.py <input_file> <input_language> <output_languages>
```

Replace `<input_file>` with the path to your input XML file containing strings to be translated.

Replace `<input_language>` with the language code of the input strings (e.g., `en` for English).

Replace `<output_languages>` with a space-separated list of language codes for the desired output languages. If not specified, the script translates to a predefined set of languages.

Example:

```bash
python translate_strings.py strings.xml en fr es
```

This command translates the strings from `strings.xml` (English) to French and Spanish.

### Using Standalone Executable (Windows)

For Windows users, simply double-click on `stringtranslator.exe` to run the translation process. Follow the on-screen instructions to input the necessary information, such as the input file, input language, and output languages.

## Additional Notes

- The `out` directory will be created to store the translated output.
- Ensure proper network connectivity for translation using Google Translate.
- Review and update the predefined set of output languages in the script as needed.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
