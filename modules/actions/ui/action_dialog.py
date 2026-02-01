"""
Action Dialog
Dialog for adding or editing actions.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox, QDateEdit, QTimeEdit,
    QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, QDate, QTime
from datetime import datetime


class ActionDialog(QDialog):
    """Dialog for adding/editing an action."""
    
    def __init__(self, action_service, action=None, parent=None):
        super().__init__(parent)
        self.action_service = action_service
        self.action = action
        self.is_edit = action is not None
        
        self.setWindowTitle("Edit Action" if self.is_edit else "Add New Action")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_action_data()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., Call Mr. Sharma about Builder X deal")
        form.addRow("Title:*", self.title_input)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form.addRow("Date:*", self.date_input)
        
        # Time
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(10, 0))  # Default 10:00 AM
        form.addRow("Time:", self.time_input)
        
        # Type
        self.type_input = QComboBox()
        self.type_input.addItems([
            "Call",
            "Meeting",
            "Site Visit",
            "Follow-up",
            "Documentation",
            "Other"
        ])
        form.addRow("Type:*", self.type_input)
        
        # Priority
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setCurrentText("Medium")
        form.addRow("Priority:*", self.priority_input)
        
        # Client Name (optional)
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Optional")
        form.addRow("Client Name:", self.client_input)
        
        # Deal ID (optional)
        self.deal_input = QLineEdit()
        self.deal_input.setPlaceholderText("Optional - Enter deal ID")
        form.addRow("Deal ID:", self.deal_input)
        
        layout.addLayout(form)
        
        # Description
        desc_label = QLabel("Description:")
        layout.addWidget(desc_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add any additional details...")
        self.description_input.setMaximumHeight(100)
        layout.addWidget(self.description_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Action")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_action)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_action_data(self):
        """Load existing action data for editing."""
        self.title_input.setText(self.action.title)
        
        # Date
        q_date = QDate(
            self.action.action_date.year,
            self.action.action_date.month,
            self.action.action_date.day
        )
        self.date_input.setDate(q_date)
        
        # Time
        if self.action.action_time:
            # action_time is stored as string "HH:MM"
            try:
                time_parts = self.action.action_time.split(':')
                if len(time_parts) == 2:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    q_time = QTime(hour, minute)
                    self.time_input.setTime(q_time)
            except (ValueError, AttributeError):
                pass  # Use default time if parsing fails
        
        # Type
        type_map = {
            'call': 'Call',
            'meeting': 'Meeting',
            'site_visit': 'Site Visit',
            'follow_up': 'Follow-up',
            'documentation': 'Documentation',
            'other': 'Other'
        }
        self.type_input.setCurrentText(type_map.get(self.action.action_type, 'Other'))
        
        # Priority
        self.priority_input.setCurrentText(self.action.priority.capitalize())
        
        # Client
        if self.action.client_name:
            self.client_input.setText(self.action.client_name)
        
        # Deal ID
        if self.action.deal_id:
            self.deal_input.setText(str(self.action.deal_id))
        
        # Description
        if self.action.description:
            self.description_input.setPlainText(self.action.description)
    
    def save_action(self):
        """Save the action."""
        # Validate
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a title.")
            self.title_input.setFocus()
            return
        
        try:
            # Prepare data
            qt_time = self.time_input.time()
            action_time_str = qt_time.toString("HH:mm")

            action_data = {
                'title': self.title_input.text().strip(),
                'action_date': self.date_input.date().toPython(),
                'action_time': action_time_str,
                'action_type': self.type_input.currentText().lower().replace(' ', '_').replace('-', '_'),
                'priority': self.priority_input.currentText().lower(),
                'client_name': self.client_input.text().strip() or None,
                'description': self.description_input.toPlainText().strip() or None,
                'completed': False
            }
            
            # Deal ID (optional)
            deal_id_text = self.deal_input.text().strip()
            if deal_id_text:
                try:
                    action_data['deal_id'] = int(deal_id_text)
                except ValueError:
                    QMessageBox.warning(self, "Validation Error", "Deal ID must be a number.")
                    return
            else:
                action_data['deal_id'] = None
            
            print(f"[DEBUG] Saving action with data: {action_data}")
            print(f"[DEBUG] Is edit mode: {self.is_edit}")
            
            # Save
            if self.is_edit:
                print(f"[DEBUG] Updating action ID: {self.action.id}")
                result = self.action_service.update(self.action.id, action_data)
                print(f"[DEBUG] Update result: {result}")
                QMessageBox.information(self, "Success", "Action updated successfully!")
            else:
                print(f"[DEBUG] Creating new action")
                result = self.action_service.create(**action_data)
                print(f"[DEBUG] Create result: {result}")
                QMessageBox.information(self, "Success", "Action created successfully!")
            
            self.accept()
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to save action")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.critical(self, "Error", f"Failed to save action: {str(e)}\n\nPlease check the console for details.")
