"""
Partner Dialog
Dialog for adding or editing business partners.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt


class PartnerDialog(QDialog):
    """Dialog for adding/editing a partner."""
    
    def __init__(self, partner_service, partner=None, parent=None):
        super().__init__(parent)
        self.partner_service = partner_service
        self.partner = partner
        self.is_edit = partner is not None
        
        self.setWindowTitle("Edit Partner" if self.is_edit else "Add New Partner")
        self.setModal(True)
        self.setMinimumWidth(550)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_partner_data()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full name")
        form.addRow("Name:*", self.name_input)
        
        # Partner Type
        self.type_input = QComboBox()
        self.type_input.addItems(["Broker", "Builder", "Channel Partner"])
        form.addRow("Partner Type:*", self.type_input)
        
        # Company Name
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Company/Firm name")
        form.addRow("Company Name:", self.company_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("10-digit phone number")
        form.addRow("Phone:*", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form.addRow("Email:", self.email_input)
        
        # Default Commission Split
        self.commission_input = QDoubleSpinBox()
        self.commission_input.setMaximum(100)
        self.commission_input.setDecimals(2)
        self.commission_input.setSuffix(" %")
        form.addRow("Commission Split:", self.commission_input)
        
        # RERA Number
        self.rera_input = QLineEdit()
        self.rera_input.setPlaceholderText("RERA registration number")
        form.addRow("RERA Number:", self.rera_input)
        
        # GST Number
        self.gst_input = QLineEdit()
        self.gst_input.setPlaceholderText("GST number")
        form.addRow("GST Number:", self.gst_input)
        
        # PAN Number
        self.pan_input = QLineEdit()
        self.pan_input.setPlaceholderText("PAN number")
        form.addRow("PAN Number:", self.pan_input)
        
        # Status
        self.status_input = QComboBox()
        self.status_input.addItems(["Active", "Inactive"])
        form.addRow("Status:*", self.status_input)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Partner")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_partner)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_partner_data(self):
        """Load existing partner data for editing."""
        self.name_input.setText(self.partner.name)
        
        # Type
        type_map = {
            'broker': 'Broker',
            'builder': 'Builder',
            'channel_partner': 'Channel Partner'
        }
        self.type_input.setCurrentText(type_map.get(self.partner.partner_type, 'Broker'))
        
        if self.partner.company_name:
            self.company_input.setText(self.partner.company_name)
        
        if self.partner.phone:
            self.phone_input.setText(self.partner.phone)
        
        if self.partner.email:
            self.email_input.setText(self.partner.email)
        
        if self.partner.default_commission_split:
            self.commission_input.setValue(self.partner.default_commission_split)
        
        if self.partner.rera_number:
            self.rera_input.setText(self.partner.rera_number)
        
        if self.partner.gst_number:
            self.gst_input.setText(self.partner.gst_number)
        
        if self.partner.pan_number:
            self.pan_input.setText(self.partner.pan_number)
        
        # Status
        self.status_input.setCurrentText(self.partner.status.title())
    
    def save_partner(self):
        """Save the partner."""
        # Validate
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a name.")
            self.name_input.setFocus()
            return
        
        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a phone number.")
            self.phone_input.setFocus()
            return
        
        # Validate phone (basic)
        phone = self.phone_input.text().strip()
        if not phone.isdigit() or len(phone) != 10:
            QMessageBox.warning(self, "Validation Error", "Phone number must be 10 digits.")
            return
        
        try:
            # Prepare data
            partner_data = {
                'name': self.name_input.text().strip(),
                'partner_type': self.type_input.currentText().lower().replace(' ', '_'),
                'company_name': self.company_input.text().strip() or None,
                'phone': phone,
                'email': self.email_input.text().strip() or None,
                'default_commission_split': self.commission_input.value() if self.commission_input.value() > 0 else None,
                'rera_number': self.rera_input.text().strip() or None,
                'gst_number': self.gst_input.text().strip() or None,
                'pan_number': self.pan_input.text().strip() or None,
                'status': self.status_input.currentText().lower()
            }
            
            print(f"[DEBUG] Saving partner with data: {partner_data}")
            print(f"[DEBUG] Is edit mode: {self.is_edit}")
            
            # Save
            if self.is_edit:
                print(f"[DEBUG] Updating partner ID: {self.partner.id}")
                result = self.partner_service.update(self.partner.id, partner_data)
                print(f"[DEBUG] Update result: {result}")
                QMessageBox.information(self, "Success", "Partner updated successfully!")
            else:
                print(f"[DEBUG] Creating new partner")
                result = self.partner_service.create(**partner_data)
                print(f"[DEBUG] Create result: {result}")
                QMessageBox.information(self, "Success", "Partner created successfully!")
            
            self.accept()
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to save partner")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(self, "Error", f"Failed to save partner: {str(e)}\n\nPlease check the console for details.")
