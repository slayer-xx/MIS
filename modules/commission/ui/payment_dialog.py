"""
Payment Dialog
Dialog for recording commission payments.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox,
    QDateEdit, QTextEdit
)
from PySide6.QtCore import Qt, QDate


class PaymentDialog(QDialog):
    """Dialog for recording a commission payment."""
    
    def __init__(self, commission_service, parent=None):
        super().__init__(parent)
        self.commission_service = commission_service
        
        self.setWindowTitle("Record Commission Payment")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        # Commission ID
        self.commission_input = QLineEdit()
        self.commission_input.setPlaceholderText("Enter commission structure ID")
        form.addRow("Commission ID:*", self.commission_input)
        
        # Amount Received
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ₹")
        form.addRow("Amount Received:*", self.amount_input)
        
        # Payment Type
        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems([
            "Cash",
            "Bank Transfer",
            "Cheque",
            "UPI",
            "Other"
        ])
        form.addRow("Payment Type:*", self.payment_type_input)
        
        # Payment Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form.addRow("Payment Date:*", self.date_input)
        
        # Reference Number
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Transaction ID, Cheque number, etc.")
        form.addRow("Reference Number:", self.reference_input)
        
        layout.addLayout(form)
        
        # Notes
        notes_label = QLabel("Notes:")
        layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any additional details about the payment...")
        self.notes_input.setMaximumHeight(80)
        layout.addWidget(self.notes_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Record Payment")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_payment)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_payment(self):
        """Save the payment record."""
        # Validate
        if not self.commission_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a commission ID.")
            self.commission_input.setFocus()
            return
        
        try:
            commission_id = int(self.commission_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Commission ID must be a number.")
            return
        
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than 0.")
            return
        
        try:
            # Prepare payment data
            payment_data = {
                'commission_structure_id': commission_id,
                'amount': self.amount_input.value(),
                'payment_type': self.payment_type_input.currentText().lower().replace(' ', '_'),
                'payment_date': self.date_input.date().toPython(),
                'reference_number': self.reference_input.text().strip() or None,
                'notes': self.notes_input.toPlainText().strip() or None
            }
            
            # Record payment (this would need a payment service method)
            # For now, we'll update the commission structure
            # Ensure commission exists
            commission = self.commission_service.get_by_id(commission_id)
            if not commission:
                QMessageBox.warning(self, "Error", "Commission structure not found.")
                return

            # Add deal_id into payment data
            payment_data['deal_id'] = commission.deal_id

            # Record payment via service
            self.commission_service.record_payment(**payment_data)

            
            QMessageBox.information(self, "Success", "Payment recorded successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record payment: {str(e)}")
