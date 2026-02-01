"""
Add Deal Dialog
Dialog window for creating new deals.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Signal
import config
from modules.deals.services.deal_service import DealService


class AddDealDialog(QDialog):
    """
    Dialog for adding a new deal.
    Emits deal_created signal when a deal is successfully created.
    """
    
    deal_created = Signal()  # Signal emitted when deal is created

    def __init__(self, deal_service, deal=None, parent=None):
        super().__init__(parent)
        self.service = deal_service
        self.deal = deal  # Store the deal for edit mode
        self.is_edit = deal is not None  # Flag to indicate edit mode
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Edit Deal" if self.is_edit else "Add New Deal")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Edit Deal" if self.is_edit else "Create New Deal")
        title_label.setProperty("cssClass", "section-title")
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Deal Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., 3BHK Apartment Sale")
        form_layout.addRow(self._create_label("Deal Title *"), self.title_input)
        
        # Deal Type
        self.deal_type_combo = QComboBox()
        self.deal_type_combo.addItems(config.DEAL_TYPES)
        form_layout.addRow(self._create_label("Deal Type *"), self.deal_type_combo)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(config.DEAL_STATUSES)
        form_layout.addRow(self._create_label("Status *"), self.status_combo)
        
        # Client Name
        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("e.g., John Doe")
        form_layout.addRow(self._create_label("Client Name *"), self.client_name_input)
        
        # Property Value
        self.property_value_input = QLineEdit()
        self.property_value_input.setPlaceholderText("e.g., 5000000")
        form_layout.addRow(self._create_label("Property Value (₹)"), self.property_value_input)
        
        # Expected Commission
        self.expected_commission_input = QLineEdit()
        self.expected_commission_input.setPlaceholderText("e.g., 100000")
        form_layout.addRow(self._create_label("Expected Commission (₹)"), self.expected_commission_input)
        
        layout.addLayout(form_layout)
        
        # Help text
        help_label = QLabel("* Required fields")
        help_label.setProperty("cssClass", "help-text")
        layout.addWidget(help_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("cssClass", "secondary")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Update Deal" if self.is_edit else "Save Deal")
        save_button.setProperty("cssClass", "success")
        save_button.clicked.connect(self.save_deal)
        save_button.setDefault(True)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Load deal data if in edit mode
        if self.is_edit:
            self.load_deal_data()

    def _create_label(self, text: str) -> QLabel:
        """Create a form label with consistent styling."""
        label = QLabel(text)
        label.setProperty("cssClass", "form-label")
        return label
    
    def load_deal_data(self):
        """Load existing deal data into the form fields."""
        if not self.deal:
            return
        
        # Populate form fields with deal data
        self.title_input.setText(self.deal.title or "")
        
        # Set combo box values
        deal_type_index = self.deal_type_combo.findText(self.deal.deal_type)
        if deal_type_index >= 0:
            self.deal_type_combo.setCurrentIndex(deal_type_index)
        
        status_index = self.status_combo.findText(self.deal.status)
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
        
        self.client_name_input.setText(self.deal.client_name or "")
        
        # Set numeric fields
        if self.deal.property_value:
            self.property_value_input.setText(str(self.deal.property_value))
        
        if self.deal.expected_commission:
            self.expected_commission_input.setText(str(self.deal.expected_commission))

    def save_deal(self):
        """Validate and save the deal (create or update)."""
        try:
            # Get form values
            title = self.title_input.text().strip()
            deal_type = self.deal_type_combo.currentText()
            status = self.status_combo.currentText()
            client_name = self.client_name_input.text().strip()
            
            # Parse numeric values
            property_value = None
            if self.property_value_input.text().strip():
                try:
                    property_value = float(self.property_value_input.text().strip())
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Invalid Input",
                        "Property value must be a valid number."
                    )
                    return
            
            expected_commission = None
            if self.expected_commission_input.text().strip():
                try:
                    expected_commission = float(self.expected_commission_input.text().strip())
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Invalid Input",
                        "Expected commission must be a valid number."
                    )
                    return
            
            if self.is_edit:
                # Update existing deal
                print(f"[DEBUG] Updating deal ID {self.deal.id} with:")
                print(f"  title={title}, deal_type={deal_type}, status={status}")
                print(f"  client_name={client_name}, property_value={property_value}")
                print(f"  expected_commission={expected_commission}")
                
                # Update deal through service
                result = self.service.update_deal(
                    self.deal.id,
                    title=title,
                    deal_type=deal_type,
                    status=status,
                    client_name=client_name,
                    property_value=property_value,
                    expected_commission=expected_commission
                )
                
                print(f"[DEBUG] Deal updated successfully: {result}")
            else:
                # Create new deal
                print(f"[DEBUG] Creating deal with:")
                print(f"  title={title}, deal_type={deal_type}, status={status}")
                print(f"  client_name={client_name}, property_value={property_value}")
                print(f"  expected_commission={expected_commission}")
                
                # Create deal through service
                result = self.service.create_deal(
                    title=title,
                    deal_type=deal_type,
                    status=status,
                    client_name=client_name,
                    property_value=property_value,
                    expected_commission=expected_commission
                )
                
                print(f"[DEBUG] Deal created successfully: {result}")
            
            # Emit signal and close
            self.deal_created.emit()
            self.accept()
            
        except ValueError as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Validation error {'updating' if self.is_edit else 'creating'} deal")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.warning(
                self,
                "Validation Error",
                str(e)
            )
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to {'update' if self.is_edit else 'create'} deal")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to {'update' if self.is_edit else 'create'} deal: {str(e)}\n\nPlease check the console for details."
            )
