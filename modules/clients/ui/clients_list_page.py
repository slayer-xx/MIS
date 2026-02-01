"""
Clients List Page
View and manage all clients with search and filtering.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QComboBox, QLineEdit,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class ClientsListPage(QWidget):
    """Clients list page with search and filtering."""
    
    client_selected = Signal(int)
    
    def __init__(self, client_service):
        super().__init__()
        self.client_service = client_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the clients list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("👥 Clients")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add client button
        add_btn = QPushButton("➕ Add New Client")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_client)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Type filter
        type_label = QLabel("Type:")
        filter_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Buyer", "Seller", "Both"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)
        
        # Status filter
        status_label = QLabel("Status:")
        filter_layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive", "Converted"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.status_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, email...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.table = self.create_clients_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def create_clients_table(self):
        """Create the clients table widget."""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Name", "Phone", "Email", "Type", "Status", "Budget Range"
        ])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        # Column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Budget
        
        # Double click to view details
        table.doubleClicked.connect(self.view_client_details)
        
        return table
    
    def load_data(self):
        """Load clients data."""
        try:
            clients = self.client_service.get_all()
            self.populate_table(clients)
        except Exception as e:
            print(f"Error loading clients: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load clients: {str(e)}")
    
    def populate_table(self, clients):
        """Populate the table with clients data."""
        self.table.setRowCount(0)
        
        for client in clients:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Name
            self.table.setItem(row, 0, QTableWidgetItem(client.name))
            
            # Phone
            self.table.setItem(row, 1, QTableWidgetItem(client.phone or '-'))
            
            # Email
            self.table.setItem(row, 2, QTableWidgetItem(client.email or '-'))
            
            # Type
            client_type = client.client_type.title()
            self.table.setItem(row, 3, QTableWidgetItem(client_type))
            
            # Status
            status_item = QTableWidgetItem(client.status.title())
            if client.status == 'active':
                status_item.setForeground(Qt.darkGreen)
            elif client.status == 'converted':
                status_item.setForeground(Qt.blue)
            else:
                status_item.setForeground(Qt.gray)
            self.table.setItem(row, 4, status_item)
            
            # Budget Range
            if client.budget_min and client.budget_max:
                budget_text = f"₹{client.budget_min/100000:.1f}L - ₹{client.budget_max/100000:.1f}L"
            elif client.budget_min:
                budget_text = f"₹{client.budget_min/100000:.1f}L+"
            elif client.budget_max:
                budget_text = f"Up to ₹{client.budget_max/100000:.1f}L"
            else:
                budget_text = '-'
            self.table.setItem(row, 5, QTableWidgetItem(budget_text))
            
            # Store client_id
            self.table.item(row, 0).setData(Qt.UserRole, client.id)
    
    def view_client_details(self, index):
        """Open edit dialog for the selected client."""
        from modules.clients.ui.client_dialog import ClientDialog
        
        row = index.row()
        item = self.table.item(row, 0)
        
        if not item:
            print("[WARNING] No item at selected row")
            return
        
        client_id = item.data(Qt.UserRole)
        if not client_id:
            print("[WARNING] No client ID found in item data")
            return
        
        try:
            print(f"[DEBUG] Opening client details for ID: {client_id}")
            client = self.client_service.get_by_id(client_id)
            if client:
                print(f"[DEBUG] Client found: {client.name}")
                dialog = ClientDialog(self.client_service, client=client, parent=self)
                result = dialog.exec()
                print(f"[DEBUG] Dialog result: {result}")
                if result:
                    self.refresh()
            else:
                print(f"[WARNING] Client with ID {client_id} not found")
                QMessageBox.warning(self, "Error", f"Client with ID {client_id} not found")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to open client details")
            print(f"Client ID: {client_id}")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.warning(self, "Error", f"Failed to open client:\n{str(e)}\n\nCheck console for details")
    def add_client(self):
        """Open add client dialog."""
        from modules.clients.ui.client_dialog import ClientDialog
        
        try:
            print("[DEBUG] Opening add client dialog")
            dialog = ClientDialog(self.client_service, parent=self)
            result = dialog.exec()
            print(f"[DEBUG] Dialog result: {result}")
            if result:
                self.refresh()
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"[ERROR] Failed to open add client dialog")
            print(f"Error: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print('='*60)
            QMessageBox.warning(self, "Error", f"Failed to open dialog:\n{str(e)}\n\nCheck console for details")
    
    def apply_filters(self):
        """Apply filters to the table."""
        try:
            # Get all clients
            clients = self.client_service.get_all()
            
            # Apply type filter
            type_filter = self.type_filter.currentText().lower()
            if type_filter != "all":
                clients = [c for c in clients if c.client_type == type_filter]
            
            # Apply status filter
            status_filter = self.status_filter.currentText().lower()
            if status_filter != "all":
                clients = [c for c in clients if c.status == status_filter]
            
            # Apply search filter
            search_text = self.search_input.text().lower().strip()
            if search_text:
                clients = [c for c in clients if 
                          search_text in c.name.lower() or
                          (c.phone and search_text in c.phone) or
                          (c.email and search_text in c.email.lower())]
            
            self.populate_table(clients)
            
        except Exception as e:
            print(f"Error applying filters: {e}")
    
    def refresh(self):
        """Refresh the clients data."""
        self.load_data()
