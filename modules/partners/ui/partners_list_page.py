"""
Partners List Page
View and manage all business partners.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QComboBox, QLineEdit,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class PartnersListPage(QWidget):
    """Partners list page with search and filtering."""
    
    partner_selected = Signal(int)
    
    def __init__(self, partner_service):
        super().__init__()
        self.partner_service = partner_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the partners list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🤝 Business Partners")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add partner button
        add_btn = QPushButton("➕ Add New Partner")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_partner)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Type filter
        type_label = QLabel("Type:")
        filter_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Broker", "Builder", "Channel Partner"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)
        
        # Status filter
        status_label = QLabel("Status:")
        filter_layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.status_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, company, phone...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.table = self.create_partners_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def create_partners_table(self):
        """Create the partners table widget."""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Name", "Type", "Company", "Phone", "Email", "Status"
        ])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        # Column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Company
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        
        # Double click to view details
        table.doubleClicked.connect(self.view_partner_details)
        
        return table
    
    def load_data(self):
        """Load partners data."""
        try:
            partners = self.partner_service.get_all()
            self.populate_table(partners)
        except Exception as e:
            print(f"Error loading partners: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load partners: {str(e)}")
    
    def populate_table(self, partners):
        """Populate the table with partners data."""
        self.table.setRowCount(0)
        
        for partner in partners:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Name
            self.table.setItem(row, 0, QTableWidgetItem(partner.name))
            
            # Type
            partner_type = partner.partner_type.replace('_', ' ').title()
            self.table.setItem(row, 1, QTableWidgetItem(partner_type))
            
            # Company
            self.table.setItem(row, 2, QTableWidgetItem(partner.company_name or '-'))
            
            # Phone
            self.table.setItem(row, 3, QTableWidgetItem(partner.phone or '-'))
            
            # Email
            self.table.setItem(row, 4, QTableWidgetItem(partner.email or '-'))
            
            # Status
            status_item = QTableWidgetItem(partner.status.title())
            if partner.status == 'active':
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setForeground(Qt.gray)
            self.table.setItem(row, 5, status_item)
            
            # Store partner_id
            self.table.item(row, 0).setData(Qt.UserRole, partner.id)
    
    def view_partner_details(self, index):
        """Open edit dialog for the selected partner."""
        from modules.partners.ui.partner_dialog import PartnerDialog
        
        row = index.row()
        item = self.table.item(row, 0)
        
        if not item:
            return
        
        partner_id = item.data(Qt.UserRole)
        if not partner_id:
            return
        
        try:
            partner = self.partner_service.get_by_id(partner_id)
            if partner:
                dialog = PartnerDialog(self.partner_service, partner=partner, parent=self)
                if dialog.exec():
                    self.refresh()
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n=== ERROR in partner details ===")
            print(f"Error: {e}")
            print(f"Traceback:\n{error_details}")
            print("=" * 50)
            QMessageBox.warning(self, "Error", f"Failed to open partner:\n{str(e)}\n\nCheck console for details")
    def add_partner(self):
        """Open add partner dialog."""
        from modules.partners.ui.partner_dialog import PartnerDialog
        
        dialog = PartnerDialog(self.partner_service, parent=self)
        if dialog.exec():
            self.refresh()
    
    def apply_filters(self):
        """Apply filters to the table."""
        try:
            # Get all partners
            partners = self.partner_service.get_all()
            
            # Apply type filter
            type_filter = self.type_filter.currentText().lower().replace(' ', '_')
            if type_filter != "all":
                partners = [p for p in partners if p.partner_type == type_filter]
            
            # Apply status filter
            status_filter = self.status_filter.currentText().lower()
            if status_filter != "all":
                partners = [p for p in partners if p.status == status_filter]
            
            # Apply search filter
            search_text = self.search_input.text().lower().strip()
            if search_text:
                partners = [p for p in partners if 
                          search_text in p.name.lower() or
                          (p.company_name and search_text in p.company_name.lower()) or
                          (p.phone and search_text in p.phone) or
                          (p.email and search_text in p.email.lower())]
            
            self.populate_table(partners)
            
        except Exception as e:
            print(f"Error applying filters: {e}")
    
    def refresh(self):
        """Refresh the partners data."""
        self.load_data()
