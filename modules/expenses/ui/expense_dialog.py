"""
Expense Dialog
Dialog for adding or editing expenses.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox,
    QDateEdit, QTextEdit, QCheckBox
)
from PySide6.QtCore import Qt, QDate


class ExpenseDialog(QDialog):
    """Dialog for adding/editing an expense."""
    
    def __init__(self, expense_service, expense=None, parent=None):
        super().__init__(parent)
        self.expense_service = expense_service
        self.expense = expense
        self.is_edit = expense is not None
        
        self.setWindowTitle("Edit Expense" if self.is_edit else "Add New Expense")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_expense_data()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Brief description of expense")
        form.addRow("Title:*", self.title_input)
        
        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ₹")
        form.addRow("Amount:*", self.amount_input)
        
        # Category
        self.category_input = QComboBox()
        self.category_input.addItems([
            "Marketing",
            "Office",
            "Travel",
            "Utilities",
            "Salary",
            "Commission",
            "Legal",
            "Other"
        ])
        form.addRow("Category:*", self.category_input)
        
        # Sub-Category
        self.sub_category_input = QLineEdit()
        self.sub_category_input.setPlaceholderText("Optional - more specific category")
        form.addRow("Sub-Category:", self.sub_category_input)
        
        # Payment Type
        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems([
            "Cash",
            "Bank Transfer",
            "Cheque",
            "UPI",
            "Credit Card",
            "Other"
        ])
        form.addRow("Payment Type:*", self.payment_type_input)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form.addRow("Date:*", self.date_input)

        
        # Vendor
        self.vendor_input = QLineEdit()
        self.vendor_input.setPlaceholderText("Vendor or payee name")
        form.addRow("Vendor Name:", self.vendor_input)
        
        # Invoice Number
        self.invoice_input = QLineEdit()
        self.invoice_input.setPlaceholderText("Invoice or bill number")
        form.addRow("Invoice Number:", self.invoice_input)
        
        # Recurring
        self.recurring_checkbox = QCheckBox("This is a recurring expense")
        form.addRow("", self.recurring_checkbox)
        
        layout.addLayout(form)
        
        # Description
        desc_label = QLabel("Description:")
        layout.addWidget(desc_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add any additional details...")
        self.description_input.setMaximumHeight(80)
        layout.addWidget(self.description_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Expense")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_expense)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_expense_data(self):
        """Load existing expense data for editing."""
        self.title_input.setText(self.expense.title)
        self.amount_input.setValue(self.expense.amount)
        
        # Category
        category_map = {
            'marketing': 'Marketing',
            'office': 'Office',
            'travel': 'Travel',
            'utilities': 'Utilities',
            'salary': 'Salary',
            'commission': 'Commission',
            'legal': 'Legal',
            'other': 'Other'
        }
        self.category_input.setCurrentText(
            category_map.get(self.expense.category, 'Other')
        )
        
        if self.expense.sub_category:
            self.sub_category_input.setText(self.expense.sub_category)
        
        # Payment Type
        payment_map = {
            'cash': 'Cash',
            'bank_transfer': 'Bank Transfer',
            'cheque': 'Cheque',
            'upi': 'UPI',
            'credit_card': 'Credit Card',
            'other': 'Other'
        }
        self.payment_type_input.setCurrentText(
            payment_map.get(self.expense.payment_type, 'Cash')
        )
        
        # Date
        q_date = QDate(
            self.expense.expense_date.year,
            self.expense.expense_date.month,
            self.expense.expense_date.day
        )
        self.date_input.setDate(q_date)
        
        if self.expense.vendor_name:
            self.vendor_input.setText(self.expense.vendor_name)
        
        if self.expense.invoice_number:
            self.invoice_input.setText(self.expense.invoice_number)
        
        if self.expense.is_recurring:
            self.recurring_checkbox.setChecked(True)
        
        if self.expense.description:
            self.description_input.setPlainText(self.expense.description)
    
    def save_expense(self):
        """Save the expense."""
        # Validate
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a title.")
            self.title_input.setFocus()
            return
        
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than 0.")
            return
        
        try:
            # Prepare data
            expense_data = {
                'title': self.title_input.text().strip(),
                'amount': self.amount_input.value(),
                'category': self.category_input.currentText().lower(),
                'sub_category': self.sub_category_input.text().strip() or None,
                'payment_type': self.payment_type_input.currentText().lower().replace(' ', '_'),
                'expense_date': self.date_input.date().toPython(),
                'vendor_name': self.vendor_input.text().strip() or None,
                'invoice_number': self.invoice_input.text().strip() or None,
                'is_recurring': self.recurring_checkbox.isChecked(),
                'description': self.description_input.toPlainText().strip() or None
            }
            
            print(f"[DEBUG] Saving expense with data: {expense_data}")
            print(f"[DEBUG] Is edit mode: {self.is_edit}")
            
            # Save
            if self.is_edit:
                print(f"[DEBUG] Updating expense ID: {self.expense.id}")
                result = self.expense_service.update(self.expense.id, expense_data)
                print(f"[DEBUG] Update result: {result}")
                QMessageBox.information(self, "Success", "Expense updated successfully!")
            else:
                print(f"[DEBUG] Creating new expense")
                result = self.expense_service.create(**expense_data)
                print(f"[DEBUG] Create result: {result}")
                QMessageBox.information(self, "Success", "Expense created successfully!")
            
            self.accept()
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to save expense")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(self, "Error", f"Failed to save expense: {str(e)}\n\nPlease check the console for details.")
