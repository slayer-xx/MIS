"""
Team Member Dialog
Dialog for adding or editing team members (employees, revenue partners, owner)
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QMessageBox, QDoubleSpinBox,
    QTextEdit, QDateEdit, QTabWidget, QWidget
)
from PySide6.QtCore import Qt, QDate
from datetime import date


class TeamMemberDialog(QDialog):
    """Dialog for adding/editing a team member."""
    
    def __init__(self, team_service, member_id=None, parent=None):
        super().__init__(parent)
        self.team_service = team_service
        self.member_id = member_id
        self.is_edit = member_id is not None
        
        self.setWindowTitle("Edit Team Member" if self.is_edit else "Add New Team Member")
        self.setModal(True)
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)
        
        self.init_ui()
        
        if self.is_edit:
            self.load_member_data()
    
    def init_ui(self):
        """Initialize the dialog UI with tabs."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("👤 Team Member Information")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # Tab 1: Basic Info
        basic_tab = self.create_basic_info_tab()
        tabs.addTab(basic_tab, "📋 Basic Info")
        
        # Tab 2: Employment Details
        employment_tab = self.create_employment_tab()
        tabs.addTab(employment_tab, "💼 Employment")
        
        # Tab 3: Financial
        financial_tab = self.create_financial_tab()
        tabs.addTab(financial_tab, "💰 Financial")
        
        # Tab 4: Legal/Bank Info
        legal_tab = self.create_legal_tab()
        tabs.addTab(legal_tab, "📄 Legal/Bank")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Team Member")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_team_member)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_basic_info_tab(self):
        """Create basic information tab."""
        widget = QWidget()
        form = QFormLayout()
        form.setSpacing(12)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full name")
        form.addRow("Name:*", self.name_input)
        
        # Member Type
        self.member_type_input = QComboBox()
        self.member_type_input.addItems(["Employee", "Revenue Partner", "Owner"])
        self.member_type_input.currentTextChanged.connect(self.on_member_type_changed)
        form.addRow("Member Type:*", self.member_type_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("10-digit phone number")
        form.addRow("Phone:*", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form.addRow("Email:", self.email_input)
        
        # Alternate Phone
        self.alternate_phone_input = QLineEdit()
        self.alternate_phone_input.setPlaceholderText("Alternate contact number")
        form.addRow("Alternate Phone:", self.alternate_phone_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("Full address")
        form.addRow("Address:", self.address_input)
        
        # City
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("City")
        form.addRow("City:", self.city_input)
        
        widget.setLayout(form)
        return widget
    
    def create_employment_tab(self):
        """Create employment details tab."""
        widget = QWidget()
        form = QFormLayout()
        form.setSpacing(12)
        
        # Employment Status
        self.employment_status_input = QComboBox()
        self.employment_status_input.addItems(["Active", "Inactive", "On Leave"])
        form.addRow("Employment Status:*", self.employment_status_input)
        
        # Joining Date
        self.joining_date_input = QDateEdit()
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDate(QDate.currentDate())
        form.addRow("Joining Date:", self.joining_date_input)
        
        # Exit Date (if applicable)
        self.exit_date_input = QDateEdit()
        self.exit_date_input.setCalendarPopup(True)
        self.exit_date_input.setDate(QDate.currentDate())
        self.exit_date_input.setEnabled(False)
        form.addRow("Exit Date:", self.exit_date_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(150)
        self.notes_input.setPlaceholderText("Any additional notes about this team member...")
        form.addRow("Notes:", self.notes_input)
        
        widget.setLayout(form)
        return widget
    
    def create_financial_tab(self):
        """Create financial details tab."""
        widget = QWidget()
        form = QFormLayout()
        form.setSpacing(12)
        
        # Instructions
        self.financial_instructions = QLabel()
        self.financial_instructions.setWordWrap(True)
        self.financial_instructions.setStyleSheet("color: #666; font-style: italic;")
        form.addRow(self.financial_instructions)
        
        # Monthly Salary (for employees)
        self.monthly_salary_input = QDoubleSpinBox()
        self.monthly_salary_input.setMaximum(9999999)
        self.monthly_salary_input.setDecimals(0)
        self.monthly_salary_input.setSuffix(" ₹")
        self.monthly_salary_label = QLabel("Monthly Salary:")
        form.addRow(self.monthly_salary_label, self.monthly_salary_input)
        
        # Commission Percentage (for employees)
        self.commission_percentage_input = QDoubleSpinBox()
        self.commission_percentage_input.setMaximum(100)
        self.commission_percentage_input.setDecimals(2)
        self.commission_percentage_input.setSuffix(" %")
        self.commission_percentage_label = QLabel("Commission %:")
        form.addRow(self.commission_percentage_label, self.commission_percentage_input)
        
        # Revenue Share Percentage (for revenue partners)
        self.revenue_share_input = QDoubleSpinBox()
        self.revenue_share_input.setMaximum(100)
        self.revenue_share_input.setDecimals(2)
        self.revenue_share_input.setSuffix(" %")
        self.revenue_share_label = QLabel("Revenue Share %:")
        form.addRow(self.revenue_share_label, self.revenue_share_input)
        
        # Initialize field visibility based on default member type
        self.on_member_type_changed(self.member_type_input.currentText())
        
        widget.setLayout(form)
        return widget
    
    def create_legal_tab(self):
        """Create legal/bank information tab."""
        widget = QWidget()
        form = QFormLayout()
        form.setSpacing(12)
        
        # PAN Number
        self.pan_input = QLineEdit()
        self.pan_input.setPlaceholderText("ABCDE1234F")
        self.pan_input.setMaxLength(10)
        form.addRow("PAN Number:", self.pan_input)
        
        # Aadhar Number
        self.aadhar_input = QLineEdit()
        self.aadhar_input.setPlaceholderText("1234 5678 9012")
        self.aadhar_input.setMaxLength(12)
        form.addRow("Aadhar Number:", self.aadhar_input)
        
        # Bank Details Section
        form.addRow(QLabel(""))  # Spacer
        bank_header = QLabel("Bank Account Details")
        bank_header.setStyleSheet("font-weight: bold; color: #333;")
        form.addRow(bank_header)
        
        # Bank Name
        self.bank_name_input = QLineEdit()
        self.bank_name_input.setPlaceholderText("Bank name")
        form.addRow("Bank Name:", self.bank_name_input)
        
        # Account Number
        self.account_number_input = QLineEdit()
        self.account_number_input.setPlaceholderText("Account number")
        form.addRow("Account Number:", self.account_number_input)
        
        # IFSC Code
        self.ifsc_input = QLineEdit()
        self.ifsc_input.setPlaceholderText("IFSC code")
        self.ifsc_input.setMaxLength(11)
        form.addRow("IFSC Code:", self.ifsc_input)
        
        widget.setLayout(form)
        return widget
    
    def on_member_type_changed(self, member_type):
        """Update financial fields based on member type."""
        is_employee = member_type == "Employee"
        is_revenue_partner = member_type == "Revenue Partner"
        is_owner = member_type == "Owner"
        
        # Show/hide appropriate fields
        self.monthly_salary_label.setVisible(is_employee)
        self.monthly_salary_input.setVisible(is_employee)
        self.commission_percentage_label.setVisible(is_employee)
        self.commission_percentage_input.setVisible(is_employee)
        
        self.revenue_share_label.setVisible(is_revenue_partner)
        self.revenue_share_input.setVisible(is_revenue_partner)
        
        # Update instructions
        if is_employee:
            self.financial_instructions.setText(
                "Employees receive fixed monthly salary + commission % on deals they close."
            )
        elif is_revenue_partner:
            self.financial_instructions.setText(
                "Revenue Partners receive a % share of company's profit from deals they close."
            )
        else:  # Owner
            self.financial_instructions.setText(
                "Owner receives 100% of company profit (no salary or revenue split)."
            )
            # Hide all financial inputs for owner
            self.monthly_salary_label.setVisible(False)
            self.monthly_salary_input.setVisible(False)
            self.commission_percentage_label.setVisible(False)
            self.commission_percentage_input.setVisible(False)
            self.revenue_share_label.setVisible(False)
            self.revenue_share_input.setVisible(False)
    
    def load_member_data(self):
        """Load existing team member data into the form."""
        try:
            member = self.team_service.get_team_member(self.member_id)
            if not member:
                QMessageBox.warning(self, "Error", "Team member not found")
                self.reject()
                return
            
            # Basic Info
            self.name_input.setText(member.name or "")
            
            # Map member_type to display text
            type_map = {
                "employee": "Employee",
                "revenue_partner": "Revenue Partner",
                "owner": "Owner"
            }
            self.member_type_input.setCurrentText(type_map.get(member.member_type, "Employee"))
            
            self.phone_input.setText(member.phone or "")
            self.email_input.setText(member.email or "")
            self.alternate_phone_input.setText(member.alternate_phone or "")
            self.address_input.setPlainText(member.address or "")
            self.city_input.setText(member.city or "")
            
            # Employment Details
            status_map = {
                "active": "Active",
                "inactive": "Inactive",
                "on_leave": "On Leave"
            }
            self.employment_status_input.setCurrentText(status_map.get(member.employment_status, "Active"))
            
            if member.joining_date:
                if isinstance(member.joining_date, str):
                    # Parse string date
                    from datetime import datetime
                    dt = datetime.strptime(member.joining_date, '%Y-%m-%d')
                    self.joining_date_input.setDate(QDate(dt.year, dt.month, dt.day))
                else:
                    self.joining_date_input.setDate(QDate(member.joining_date.year, 
                                                          member.joining_date.month,
                                                          member.joining_date.day))
            
            if member.exit_date:
                self.exit_date_input.setEnabled(True)
                if isinstance(member.exit_date, str):
                    from datetime import datetime
                    dt = datetime.strptime(member.exit_date, '%Y-%m-%d')
                    self.exit_date_input.setDate(QDate(dt.year, dt.month, dt.day))
                else:
                    self.exit_date_input.setDate(QDate(member.exit_date.year,
                                                       member.exit_date.month,
                                                       member.exit_date.day))
            
            self.notes_input.setPlainText(member.notes or "")
            
            # Financial
            if member.monthly_salary:
                self.monthly_salary_input.setValue(member.monthly_salary)
            if member.commission_percentage:
                self.commission_percentage_input.setValue(member.commission_percentage)
            if member.revenue_share_percentage:
                self.revenue_share_input.setValue(member.revenue_share_percentage)
            
            # Legal/Bank
            self.pan_input.setText(member.pan_number or "")
            self.aadhar_input.setText(member.aadhar_number or "")
            self.bank_name_input.setText(member.bank_name or "")
            self.account_number_input.setText(member.bank_account_number or "")
            self.ifsc_input.setText(member.bank_ifsc_code or "")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load team member: {str(e)}")
    
    def save_team_member(self):
        """Validate and save the team member."""
        # Validation
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a name")
            return
        
        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a phone number")
            return
        
        try:
            # Map display text to member_type
            type_map = {
                "Employee": "employee",
                "Revenue Partner": "revenue_partner",
                "Owner": "owner"
            }
            
            status_map = {
                "Active": "active",
                "Inactive": "inactive",
                "On Leave": "on_leave"
            }
            
            # Prepare data
            data = {
                "name": self.name_input.text().strip(),
                "member_type": type_map[self.member_type_input.currentText()],
                "phone": self.phone_input.text().strip(),
                "email": self.email_input.text().strip() or None,
                "alternate_phone": self.alternate_phone_input.text().strip() or None,
                "address": self.address_input.toPlainText().strip() or None,
                "city": self.city_input.text().strip() or None,
                "employment_status": status_map[self.employment_status_input.currentText()],
                "joining_date": self.joining_date_input.date().toPython(),
                "exit_date": self.exit_date_input.date().toPython() if self.exit_date_input.isEnabled() else None,
                "notes": self.notes_input.toPlainText().strip() or None,
                "pan_number": self.pan_input.text().strip() or None,
                "aadhar_number": self.aadhar_input.text().strip() or None,
                "bank_name": self.bank_name_input.text().strip() or None,
                "bank_account_number": self.account_number_input.text().strip() or None,
                "bank_ifsc_code": self.ifsc_input.text().strip() or None,
            }
            
            # Financial fields based on type
            if data["member_type"] == "employee":
                data["monthly_salary"] = self.monthly_salary_input.value() if self.monthly_salary_input.value() > 0 else None
                data["commission_percentage"] = self.commission_percentage_input.value() if self.commission_percentage_input.value() > 0 else None
                data["revenue_share_percentage"] = None
            elif data["member_type"] == "revenue_partner":
                data["monthly_salary"] = None
                data["commission_percentage"] = None
                data["revenue_share_percentage"] = self.revenue_share_input.value() if self.revenue_share_input.value() > 0 else None
            else:  # owner
                data["monthly_salary"] = None
                data["commission_percentage"] = None
                data["revenue_share_percentage"] = None
            
            # Save
            if self.is_edit:
                self.team_service.update_team_member(self.member_id, data)
                QMessageBox.information(self, "Success", "Team member updated successfully")
            else:
                self.team_service.create_team_member(data)
                QMessageBox.information(self, "Success", "Team member added successfully")
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save team member: {str(e)}")
