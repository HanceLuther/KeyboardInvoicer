import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT

class InvoicePDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.styles = getSampleStyleSheet()
        self.elements = []

    def add_header(self, company_name):
        # At this section we are going to add company name
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        self.elements.append(Paragraph(company_name, header_style))
        
        # At this section we are going to add Invoice title
        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_LEFT
        )
        self.elements.append(Paragraph("INVOICE", title_style))

    def add_invoice_info(self, invoice_number, date):
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        self.elements.append(Paragraph(f"Invoice Number: {invoice_number}", info_style))
        self.elements.append(Paragraph(f"Date: {date}", info_style))

    def add_address_and_payment_info(self, bill_to, payment_info):
        address_style = ParagraphStyle(
            'AddressStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
        
        # Create headers
        bill_to_header = Paragraph("BILL TO:", address_style)
        payment_info_header = Paragraph("PAYMENT INFORMATION:", address_style)
        
        # Create content
        bill_to_content = [Paragraph(line, address_style) for line in bill_to]
        payment_info_content = [Paragraph(line, address_style) for line in payment_info]
        
        # Create tables for each section
        bill_to_table = Table([[bill_to_header]] + [[content] for content in bill_to_content])
        payment_info_table = Table([[payment_info_header]] + [[content] for content in payment_info_content])
        
        # Create main table containing both sections
        main_table = Table([[bill_to_table, payment_info_table]], colWidths=[3*inch, 3*inch])
        main_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('RIGHTPADDING', (0, 0), (0, 0), 30),
        ]))
        
        self.elements.append(main_table)

    def add_items_table(self, items):
        # Table header
        table_data = [["ITEM", "DESCRIPTION", "RATE", "AMOUNT"]]
        
        # Add items
        for idx, (desc, rate, amount) in enumerate(items, 1):
            table_data.append([str(idx), desc, f"${rate:,.2f}", f"${amount:,.2f}"])
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 1.5*inch, 1.5*inch])
        
        # Add style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14365D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        self.elements.append(table)

    def add_totals(self, subtotal, tax, total):
        # Create right-aligned totals
        totals_style = ParagraphStyle(
            'TotalsStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_RIGHT
        )
        
        totals_table = Table([
            ["Sub Total:", f"${subtotal:,.2f}"],
            ["Sales Tax:", f"${tax:,.2f}"],
            ["TOTAL:", f"${total:,.2f}"]
        ], colWidths=[6*inch, 1*inch])
        
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (-1, -1), (-1, -1), 12),
            ('TOPPADDING', (-1, -1), (-1, -1), 12),
        ]))
        
        self.elements.append(totals_table)

    def add_terms(self, terms):
        terms_style = ParagraphStyle(
            'TermsStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=30,
            spaceAfter=30
        )
        self.elements.append(Paragraph("TERMS AND CONDITIONS:", terms_style))
        self.elements.append(Paragraph(terms, terms_style))

    def generate(self):
        self.doc.build(self.elements)

class InvoiceGame:
    def __init__(self):
        self.invoice_data = {}
        self.styles = getSampleStyleSheet()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, message):
        self.clear_screen()
        print("\n" + "="*50)
        print(f"\n{message}\n")
        print("="*50 + "\n")
        
    def get_validated_input(self, prompt, validation_type="text"):
        while True:
            value = input(prompt).strip()
            if not value:
                print("This field cannot be empty. Please try again.")
                continue
                
            if validation_type == "number":
                try:
                    return float(value)
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                    
            if validation_type == "date":
                try:
                    return datetime.strptime(value, "%Y-%m-%d").strftime("%B %d, %Y")
                except ValueError:
                    print("Please enter a valid date in YYYY-MM-DD format.")
                    continue
                    
            return value
            
    def collect_header_info(self):
        self.print_header("🏢 COMPANY INFORMATION")
        print("Let's start with your company details!\n")
        
        self.invoice_data['company_name'] = self.get_validated_input("Enter your company name: ")
        self.invoice_data['invoice_number'] = self.get_validated_input("Enter invoice number (e.g., INV-01234): ")
        self.invoice_data['date'] = self.get_validated_input("Enter invoice date (YYYY-MM-DD): ", "date")
        
    def collect_address_info(self):
        self.print_header("📫 BILLING INFORMATION")
        print("Now, let's get the billing details!\n")
        
        self.invoice_data['bill_to'] = {
            'name': self.get_validated_input("Enter client company name: "),
            'street': self.get_validated_input("Enter street address: "),
            'city': self.get_validated_input("Enter city: "),
            'state': self.get_validated_input("Enter state: "),
            'zip': self.get_validated_input("Enter ZIP code: ")
        }
        
        print("\n🏦 Payment Information\n")
        self.invoice_data['payment_info'] = {
            'bank': self.get_validated_input("Enter bank name: "),
            'name': self.get_validated_input("Enter account holder name: "),
            'account': self.get_validated_input("Enter account number: ")
        }
        
    def collect_items(self):
        self.print_header("📝 SERVICE ITEMS")
        print("Let's add your service items! (Enter 'done' for description when finished)\n")
        
        items = []
        item_num = 1
        
        while True:
            print(f"\nItem #{item_num}")
            description = self.get_validated_input("Enter service description (or 'done' to finish): ")
            
            if description.lower() == 'done':
                if not items:
                    print("Please add at least one item!")
                    continue
                break
                
            rate = self.get_validated_input("Enter rate ($): ", "number")
            amount = rate  # In this case amount equals rate, but you could make it different
                           # if you have any advice on how to enhance this you are kindly welcome. 
            
            items.append({
                'description': description,
                'rate': rate,
                'amount': amount
            })
            
            item_num += 1
            
        self.invoice_data['items'] = items
        
    def calculate_totals(self):
        subtotal = sum(item['amount'] for item in self.invoice_data['items'])
        tax_rate = self.get_validated_input("\nEnter sales tax rate (%): ", "number") / 100
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        self.invoice_data['totals'] = {
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }
        
    def collect_terms(self):
        self.print_header("📜 TERMS AND CONDITIONS")
        self.invoice_data['terms'] = self.get_validated_input("Enter payment terms: ")
        
    def generate_pdf(self):
        generator = InvoicePDFGenerator("generated_invoice.pdf")
        generator.add_header(self.invoice_data['company_name'])
        generator.add_invoice_info(self.invoice_data['invoice_number'], self.invoice_data['date'])
        
        bill_to = [
            self.invoice_data['bill_to']['name'],
            self.invoice_data['bill_to']['street'],
            f"{self.invoice_data['bill_to']['city']}, {self.invoice_data['bill_to']['state']} {self.invoice_data['bill_to']['zip']}"
        ]
        
        payment_info = [
            f"Bank: {self.invoice_data['payment_info']['bank']}",
            f"Name: {self.invoice_data['payment_info']['name']}",
            f"Account: {self.invoice_data['payment_info']['account']}"
        ]
        
        generator.add_address_and_payment_info(bill_to, payment_info)
        
        items = [(item['description'], item['rate'], item['amount']) 
                for item in self.invoice_data['items']]
        generator.add_items_table(items)
        
        generator.add_totals(
            self.invoice_data['totals']['subtotal'],
            self.invoice_data['totals']['tax'],
            self.invoice_data['totals']['total']
        )
        
        generator.add_terms(self.invoice_data['terms'])
        generator.generate()
        
    def play(self):
        print("\n🎮 Welcome to the Interactive Invoice Generator! 🎮\n")
        input("Press Enter to start your invoice creation journey...")
        
        self.collect_header_info()
        self.collect_address_info()
        self.collect_items()
        self.calculate_totals()
        self.collect_terms()
        
        self.print_header("🎉 GENERATING INVOICE")
        print("Creating your professional invoice PDF...")
        self.generate_pdf()
        print("\n✨ Success! Your invoice has been generated as 'generated_invoice.pdf'")

if __name__ == "__main__":
    game = InvoiceGame()
    game.play()