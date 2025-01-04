# KeyboardInvoicer 🎮⌨️

A keyboard-centric, interactive CLI tool for generating professional PDF invoices without ever leaving your terminal.

## 🌟 Features

- Interactive CLI interface with clear sections and emojis
- Keyboard-driven workflow - no mouse needed!
- Professional PDF output with custom styling
- Dynamic item entry and calculations
- Input validation for all fields
- Automatic tax calculations
- Clean, professional invoice layout

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/HanceLuther/KeyboardInvoicer.git
cd KeyboardInvoicer
```

2. Create and activate a virtual environment:
```bash
python -m venv invenv
source invenv/bin/activate  # On Windows use: invenv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Activate your virtual environment if not already active:
```bash
source invenv/bin/activate  # On Windows use: invenv\Scripts\activate
```

2. Run the program:
```bash
python src/invoice_generator.py
```

3. Follow the interactive prompts to create your invoice:
   - Enter company information
   - Add billing details
   - Input service items
   - Set tax rate
   - Define payment terms

4. Find your generated PDF in the current directory as 'generated_invoice.pdf'

## 📁 Project Structure

```
KeyboardInvoicer/
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   └── invoice_generator.py
└── output/
    └── sample_invoice.pdf
```

## 🔧 Requirements

- Python 3.8+
- reportlab

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- ReportLab library for PDF generation
- All the keyboard warriors who inspired this project

## 📞 Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/HanceLuther/KeyboardInvoicer/issues) on GitHub.