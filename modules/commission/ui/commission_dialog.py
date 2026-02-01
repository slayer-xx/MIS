"""
Commission Dialog
Dialog for adding or editing commission structures.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt


class CommissionDialog(QDialog):
    """Dialog for adding/editing a commission structure."""
    
    def __init__(self, commission_service, commission=None, parent=None):
        super().__init__(parent)
        self.commission_service = commission_service
        self.commission = commission
        self.is_edit = commission is not None
        
        self.setWindowTitle("Edit Commission" if self.is_edit else "Add Commission Structure")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_commission_data()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        # Deal ID
        self.deal_input = QLineEdit()
        self.deal_input.setPlaceholderText("Enter deal ID")
        form.addRow("Deal ID:*", self.deal_input)
        
        # Party Type
        self.party_type_input = QComboBox()
        self.party_type_input.addItems([
            "Self",
            "Partner",
            "Builder",
            "Channel Partner"
        ])
        form.addRow("Party Type:*", self.party_type_input)
        
        # Party Name
        self.party_name_input = QLineEdit()
        self.party_name_input.setPlaceholderText("Enter party name")
        form.addRow("Party Name:", self.party_name_input)
        
        # Amount Type
        self.amount_type_input = QComboBox()
        self.amount_type_input.addItems(["Fixed Amount", "Percentage"])
        self.amount_type_input.currentTextChanged.connect(self.on_amount_type_changed)
        form.addRow("Amount Type:*", self.amount_type_input)
        
        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ₹")
        form.addRow("Amount:*", self.amount_input)
        
        # Percentage (initially hidden)
        self.percentage_input = QDoubleSpinBox()
        self.percentage_input.setMaximum(100)
        self.percentage_input.setDecimals(2)
        self.percentage_input.setSuffix(" %")
        self.percentage_input.setVisible(False)
        self.percentage_label = QLabel("Percentage:*")
        self.percentage_label.setVisible(False)
        form.addRow(self.percentage_label, self.percentage_input)
        
        # Status
        self.status_input = QComboBox()
        self.status_input.addItems([
            "Pending",
            "Partially Received",
            "Received"
        ])
        form.addRow("Status:*", self.status_input)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Commission")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_commission)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_amount_type_changed(self, amount_type):
        """Handle amount type change."""
        if amount_type == "Percentage":
            self.amount_input.setVisible(False)
            self.percentage_input.setVisible(True)
            self.percentage_label.setVisible(True)
        else:
            self.amount_input.setVisible(True)
            self.percentage_input.setVisible(False)
            self.percentage_label.setVisible(False)
    
    def load_commission_data(self):
        """Load existing commission data for editing."""
        self.deal_input.setText(str(self.commission.deal_id))
        
        # Party type
        party_type_map = {
            'self': 'Self',
            'partner': 'Partner',
            'builder': 'Builder',
            'channel_partner': 'Channel Partner'
        }
        self.party_type_input.setCurrentText(
            party_type_map.get(self.commission.party_type, 'Self')
        )
        
        # Party name
        if self.commission.party_name:
            self.party_name_input.setText(self.commission.party_name)
        
        # Amount/Percentage
        if self.commission.commission_percentage:
            self.amount_type_input.setCurrentText("Percentage")
            self.percentage_input.setValue(self.commission.commission_percentage)
        else:
            self.amount_type_input.setCurrentText("Fixed Amount")
            self.amount_input.setValue(self.commission.commission_amount)
        
        # Status
        status_map = {
            'pending': 'Pending',
            'partially_received': 'Partially Received',
            'received': 'Received'
        }
        self.status_input.setCurrentText(
            status_map.get(self.commission.status, 'Pending')
        )
    
    def save_commission(self):
        """Save the commission structure."""
        # Validate
        if not self.deal_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a deal ID.")
            self.deal_input.setFocus()
            return
        
        try:
            deal_id = int(self.deal_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Deal ID must be a number.")
            return
        
        try:
            # Prepare data
            commission_data = {
                'deal_id': deal_id,
                'party_type': self.party_type_input.currentText().lower().replace(' ', '_'),
                'party_name': self.party_name_input.text().strip() or None,
                'status': self.status_input.currentText().lower().replace(' ', '_')
            }
            
            # Amount or Percentage
            if self.amount_type_input.currentText() == "Percentage":
                commission_data['commission_percentage'] = self.percentage_input.value()
                # For now, we'll need the deal amount to calculate the actual amount
                # This should ideally be fetched from the deal
                commission_data['commission_amount'] = 0  # Will be calculated
            else:
                commission_data['commission_amount'] = self.amount_input.value()
                commission_data['commission_percentage'] = None
            
            print(f"[DEBUG] Saving commission with data: {commission_data}")
            print(f"[DEBUG] Is edit mode: {self.is_edit}")
            
            # Save
            if self.is_edit:
                print(f"[DEBUG] Updating commission ID: {self.commission.id}")
                result = self.commission_service.update(self.commission.id, commission_data)
                print(f"[DEBUG] Update result: {result}")
                QMessageBox.information(self, "Success", "Commission updated successfully!")
            else:
                print(f"[DEBUG] Creating new commission")
                result = self.commission_service.create(**commission_data)
                print(f"[DEBUG] Create result: {result}")
                QMessageBox.information(self, "Success", "Commission structure created successfully!")
            
            self.accept()
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to save commission")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(self, "Error", f"Failed to save commission: {str(e)}\n\nPlease check the console for details.")
