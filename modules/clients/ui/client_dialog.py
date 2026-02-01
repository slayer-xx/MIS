"""
Client Dialog
Dialog for adding or editing clients.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox,
    QTextEdit
)
from PySide6.QtCore import Qt


class ClientDialog(QDialog):
    """Dialog for adding/editing a client."""
    
    def __init__(self, client_service, client=None, parent=None):
        super().__init__(parent)
        self.client_service = client_service
        self.client = client
        self.is_edit = client is not None
        
        self.setWindowTitle("Edit Client" if self.is_edit else "Add New Client")
        self.setModal(True)
        self.setMinimumWidth(550)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_client_data()
    
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
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("10-digit phone number")
        form.addRow("Phone:*", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form.addRow("Email:", self.email_input)
        
        # Client Type
        self.type_input = QComboBox()
        self.type_input.addItems(["Buyer", "Seller", "Both"])
        form.addRow("Client Type:*", self.type_input)
        
        # Status
        self.status_input = QComboBox()
        self.status_input.addItems(["Active", "Inactive", "Converted"])
        form.addRow("Status:*", self.status_input)
        
        # Budget Range
        budget_layout = QHBoxLayout()
        budget_layout.setSpacing(10)
        
        self.budget_min_input = QDoubleSpinBox()
        self.budget_min_input.setMaximum(999999999)
        self.budget_min_input.setDecimals(0)
        self.budget_min_input.setSuffix(" ₹")
        self.budget_min_input.setPrefix("Min: ")
        budget_layout.addWidget(self.budget_min_input)
        
        self.budget_max_input = QDoubleSpinBox()
        self.budget_max_input.setMaximum(999999999)
        self.budget_max_input.setDecimals(0)
        self.budget_max_input.setSuffix(" ₹")
        self.budget_max_input.setPrefix("Max: ")
        budget_layout.addWidget(self.budget_max_input)
        
        form.addRow("Budget Range:", budget_layout)
        
        # Preferred Locations
        self.locations_input = QLineEdit()
        self.locations_input.setPlaceholderText("e.g., Sector 50, Golf Course Road")
        form.addRow("Preferred Locations:", self.locations_input)
        
        # Property Types
        self.property_types_input = QLineEdit()
        self.property_types_input.setPlaceholderText("e.g., Apartment, Villa, Plot")
        form.addRow("Property Types:", self.property_types_input)
        
        # Source
        self.source_input = QComboBox()
        self.source_input.addItems([
            "Walk-in",
            "Referral",
            "Website",
            "Social Media",
            "Advertisement",
            "Other"
        ])
        form.addRow("Source:", self.source_input)
        
        layout.addLayout(form)
        
        # Notes
        notes_label = QLabel("Notes:")
        layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any additional notes about the client...")
        self.notes_input.setMaximumHeight(80)
        layout.addWidget(self.notes_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Client")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_client)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_client_data(self):
        """Load existing client data for editing."""
        self.name_input.setText(self.client.name)
        
        if self.client.phone:
            self.phone_input.setText(self.client.phone)
        
        if self.client.email:
            self.email_input.setText(self.client.email)
        
        # Type
        self.type_input.setCurrentText(self.client.client_type.title())
        
        # Status
        self.status_input.setCurrentText(self.client.status.title())
        
        # Budget
        if self.client.budget_min:
            self.budget_min_input.setValue(self.client.budget_min)
        
        if self.client.budget_max:
            self.budget_max_input.setValue(self.client.budget_max)
        
        # Locations
        if self.client.preferred_locations:
            self.locations_input.setText(self.client.preferred_locations)
        
        # Property Types
        if self.client.preferred_property_types:
            self.property_types_input.setText(self.client.preferred_property_types)
        
        # Source
        if self.client.source:
            source_map = {
                'walk_in': 'Walk-in',
                'referral': 'Referral',
                'website': 'Website',
                'social_media': 'Social Media',
                'advertisement': 'Advertisement',
                'other': 'Other'
            }
            self.source_input.setCurrentText(
                source_map.get(self.client.source, 'Other')
            )
    
    def save_client(self):
        """Save the client."""
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
            client_data = {
                'name': self.name_input.text().strip(),
                'phone': phone,
                'email': self.email_input.text().strip() or None,
                'client_type': self.type_input.currentText().lower(),
                'status': self.status_input.currentText().lower(),
                'budget_min': self.budget_min_input.value() if self.budget_min_input.value() > 0 else None,
                'budget_max': self.budget_max_input.value() if self.budget_max_input.value() > 0 else None,
                'preferred_locations': self.locations_input.text().strip() or None,
                'preferred_property_types': self.property_types_input.text().strip() or None,
                'source': self.source_input.currentText().lower().replace(' ', '_').replace('-', '_')
            }
            
            print(f"[DEBUG] Saving client with data: {client_data}")
            print(f"[DEBUG] Is edit mode: {self.is_edit}")
            
            # Save
            if self.is_edit:
                print(f"[DEBUG] Updating client ID: {self.client.id}")
                result = self.client_service.update(self.client.id, client_data)
                print(f"[DEBUG] Update result: {result}")
                QMessageBox.information(self, "Success", "Client updated successfully!")
            else:
                print(f"[DEBUG] Creating new client")
                result = self.client_service.create(**client_data)
                print(f"[DEBUG] Create result: {result}")
                QMessageBox.information(self, "Success", "Client created successfully!")
            
            self.accept()
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to save client")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(self, "Error", f"Failed to save client: {str(e)}\n\nPlease check the console for details.")
