"""
Team Members List Page
View and manage all team members (employees, revenue partners, owner)
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QComboBox, QLineEdit,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class TeamListPage(QWidget):
    """Team members list page with search and filtering."""
    
    team_member_selected = Signal(int)
    
    def __init__(self, team_service):
        super().__init__()
        self.team_service = team_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the team list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("👥 Team Members")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add team member button
        add_btn = QPushButton("➕ Add Team Member")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_team_member)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Type filter
        type_label = QLabel("Type:")
        filter_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Employee", "Revenue Partner", "Owner"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)
        
        # Status filter
        status_label = QLabel("Status:")
        filter_layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive", "On Leave"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.status_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, email...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Summary stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.total_label = QLabel("Total: 0")
        self.total_label.setObjectName("statLabel")
        stats_layout.addWidget(self.total_label)
        
        self.employees_label = QLabel("Employees: 0")
        self.employees_label.setObjectName("statLabel")
        stats_layout.addWidget(self.employees_label)
        
        self.partners_label = QLabel("Revenue Partners: 0")
        self.partners_label.setObjectName("statLabel")
        stats_layout.addWidget(self.partners_label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Table
        self.table = self.create_team_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def create_team_table(self):
        """Create the team members table widget."""
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "Name", "Type", "Phone", "Email", "Status", 
            "Deals Closed", "Commission Earned", "Salary/Share %"
        ])
        
        # Configure table
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Deals
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Commission
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Salary/Share
        
        # Connect double-click
        table.cellDoubleClicked.connect(self.on_row_double_clicked)
        
        # Context menu
        table.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        return table
    
    def load_data(self):
        """Load team members data into the table."""
        try:
            # Get all team members
            team_members = self.team_service.get_all_team_members()
            
            # Update stats
            self.update_stats(team_members)
            
            # Store current members
            self.current_members = team_members
            
            # Apply filters
            self.apply_filters()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load team members: {str(e)}")
    
    def update_stats(self, team_members):
        """Update summary statistics."""
        total = len(team_members)
        employees = len([m for m in team_members if m.member_type == 'employee'])
        partners = len([m for m in team_members if m.member_type == 'revenue_partner'])
        
        self.total_label.setText(f"Total: {total}")
        self.employees_label.setText(f"Employees: {employees}")
        self.partners_label.setText(f"Revenue Partners: {partners}")
    
    def apply_filters(self):
        """Apply filters to the table."""
        if not hasattr(self, 'current_members'):
            return
        
        # Get filter values
        type_filter = self.type_filter.currentText()
        status_filter = self.status_filter.currentText()
        search_text = self.search_input.text().lower()
        
        # Filter data
        filtered_members = self.current_members
        
        # Type filter
        if type_filter != "All":
            type_map = {
                "Employee": "employee",
                "Revenue Partner": "revenue_partner",
                "Owner": "owner"
            }
            filtered_members = [m for m in filtered_members if m.member_type == type_map.get(type_filter)]
        
        # Status filter
        if status_filter != "All":
            status_map = {
                "Active": "active",
                "Inactive": "inactive",
                "On Leave": "on_leave"
            }
            filtered_members = [m for m in filtered_members if m.employment_status == status_map.get(status_filter)]
        
        # Search filter
        if search_text:
            filtered_members = [
                m for m in filtered_members
                if search_text in m.name.lower() or
                   (m.phone and search_text in m.phone.lower()) or
                   (m.email and search_text in m.email.lower())
            ]
        
        # Populate table
        self.populate_table(filtered_members)
    
    def populate_table(self, team_members):
        """Populate the table with team members."""
        self.table.setRowCount(0)
        
        for member in team_members:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Name
            name_item = QTableWidgetItem(member.name)
            name_item.setData(Qt.UserRole, member.id)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_map = {
                "employee": "👤 Employee",
                "revenue_partner": "🤝 Revenue Partner",
                "owner": "👑 Owner"
            }
            type_item = QTableWidgetItem(type_map.get(member.member_type, member.member_type))
            self.table.setItem(row, 1, type_item)
            
            # Phone
            phone_item = QTableWidgetItem(member.phone or "-")
            self.table.setItem(row, 2, phone_item)
            
            # Email
            email_item = QTableWidgetItem(member.email or "-")
            self.table.setItem(row, 3, email_item)
            
            # Status
            status_map = {
                "active": "✅ Active",
                "inactive": "❌ Inactive",
                "on_leave": "🏖️ On Leave"
            }
            status_item = QTableWidgetItem(status_map.get(member.employment_status, member.employment_status))
            self.table.setItem(row, 4, status_item)
            
            # Deals Closed
            deals_item = QTableWidgetItem(str(member.total_deals_closed))
            deals_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, deals_item)
            
            # Commission Earned
            commission_item = QTableWidgetItem(f"₹{member.total_commission_earned:,.0f}")
            commission_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 6, commission_item)
            
            # Salary/Share %
            if member.member_type == 'employee':
                salary_text = f"₹{member.monthly_salary:,.0f}" if member.monthly_salary else "-"
                if member.commission_percentage:
                    salary_text += f" + {member.commission_percentage}%"
            elif member.member_type == 'revenue_partner':
                salary_text = f"{member.revenue_share_percentage}% share" if member.revenue_share_percentage else "-"
            else:
                salary_text = "N/A"
            
            salary_item = QTableWidgetItem(salary_text)
            salary_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 7, salary_item)
    
    def on_row_double_clicked(self, row, column):
        """Handle double-click on a row."""
        member_id = self.table.item(row, 0).data(Qt.UserRole)
        self.edit_team_member(member_id)
    
    def add_team_member(self):
        """Open dialog to add a new team member."""
        from modules.team.ui.team_dialog import TeamMemberDialog
        
        dialog = TeamMemberDialog(self.team_service, parent=self)
        if dialog.exec():
            self.load_data()
    
    def edit_team_member(self, member_id):
        """Open dialog to edit a team member."""
        from modules.team.ui.team_dialog import TeamMemberDialog
        
        dialog = TeamMemberDialog(self.team_service, member_id=member_id, parent=self)
        if dialog.exec():
            self.load_data()
    
    def delete_team_member(self, member_id):
        """Delete a team member."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this team member?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.team_service.delete_team_member(member_id)
                self.load_data()
                QMessageBox.information(self, "Success", "Team member deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete team member: {str(e)}")
