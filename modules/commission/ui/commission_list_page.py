"""
Commission List Page
View and manage commission structures and payments.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QTabWidget, QComboBox,
    QLineEdit, QFrame, QMessageBox
)
from modules.commission.repositories.commission_repository import CommissionPaymentRepository
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class CommissionListPage(QWidget):
    """Commission list page with pending and received tabs."""
    
    commission_selected = Signal(int)
    
    def __init__(self, commission_service, deal_service=None):
        super().__init__()
        self.commission_service = commission_service
        self.deal_service = deal_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the commission list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("💰 Commission Tracking")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add buttons
        add_structure_btn = QPushButton("➕ Add Commission Structure")
        add_structure_btn.setObjectName("primaryButton")
        add_structure_btn.clicked.connect(self.add_commission_structure)
        header_layout.addWidget(add_structure_btn)
        
        record_payment_btn = QPushButton("💵 Record Payment")
        record_payment_btn.setObjectName("secondaryButton")
        record_payment_btn.clicked.connect(self.record_payment)
        header_layout.addWidget(record_payment_btn)
        
        layout.addLayout(header_layout)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        self.total_expected_card = self.create_summary_card("Total Expected", "₹0")
        summary_layout.addWidget(self.total_expected_card)
        
        self.total_received_card = self.create_summary_card("Total Received", "₹0")
        summary_layout.addWidget(self.total_received_card)
        
        self.outstanding_card = self.create_summary_card("Outstanding", "₹0")
        summary_layout.addWidget(self.outstanding_card)
        
        layout.addLayout(summary_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Party filter
        party_label = QLabel("Party:")
        filter_layout.addWidget(party_label)
        
        self.party_filter = QComboBox()
        self.party_filter.addItems(["All", "Self", "Partner", "Builder", "Channel Partner"])
        self.party_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.party_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by party name or deal...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Pending tab
        self.pending_table = self.create_commission_table()
        self.tabs.addTab(self.pending_table, "⏳ Pending")
        
        # Received tab
        self.received_table = self.create_commission_table()
        self.tabs.addTab(self.received_table, "✅ Received")
        
        # All tab
        self.all_table = self.create_commission_table()
        self.tabs.addTab(self.all_table, "📋 All")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def create_summary_card(self, title, value):
        """Create a summary card widget."""
        frame = QFrame()
        frame.setObjectName("summaryCard")
        frame.setFrameShape(QFrame.Box)
        
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(15, 10, 15, 10)
        card_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        card_layout.addWidget(value_label)
        
        frame.setLayout(card_layout)
        frame.value_label = value_label  # Store reference for updates
        return frame
    
    def create_commission_table(self):
        """Create a commission table widget."""
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "Commission ID", "Deal ID", "Party Type", "Party Name",
            "Amount", "Status", "Received", "Outstanding"
        ])

        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        # Column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Commission ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Deal ID
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Party Type
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Party Name
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Amount
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Received
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Outstanding

        
        # Double click to view details
        table.doubleClicked.connect(self.view_commission_details)
        
        return table
    
    def load_data(self):
        """Load commission data."""
        self.load_summary()
        self.load_pending_commissions()
        self.load_received_commissions()
        self.load_all_commissions()
    
    def load_summary(self):
        """Load summary statistics."""
        try:
            commissions = self.commission_service.get_all()
            payment_repo = CommissionPaymentRepository()

            total_expected = sum(c.commission_amount for c in commissions)
            total_received = sum(
                sum(p.amount for p in payment_repo.get_by_commission_id(c.id))
                for c in commissions
            )
            outstanding = total_expected - total_received

            self.total_expected_card.value_label.setText(self.format_currency(total_expected))
            self.total_received_card.value_label.setText(self.format_currency(total_received))
            self.outstanding_card.value_label.setText(self.format_currency(outstanding))

        except Exception as e:
            print(f"Error loading summary: {e}")

    
    def load_pending_commissions(self):
        """Load pending commissions."""
        try:
            commissions = self.commission_service.get_pending()
            self.populate_table(self.pending_table, commissions)
            
            # Update tab title
            count = len(commissions)
            self.tabs.setTabText(0, f"⏳ Pending ({count})")
            
        except Exception as e:
            print(f"Error loading pending commissions: {e}")
    
    def load_received_commissions(self):
        """Load received commissions."""
        try:
            commissions = self.commission_service.get_received()
            self.populate_table(self.received_table, commissions)
            
            # Update tab title
            count = len(commissions)
            self.tabs.setTabText(1, f"✅ Received ({count})")
            
        except Exception as e:
            print(f"Error loading received commissions: {e}")
    
    def load_all_commissions(self):
        """Load all commissions."""
        try:
            commissions = self.commission_service.get_all()
            self.populate_table(self.all_table, commissions)
            
            # Update tab title
            count = len(commissions)
            self.tabs.setTabText(2, f"📋 All ({count})")
            
        except Exception as e:
            print(f"Error loading all commissions: {e}")
    
    def populate_table(self, table, commissions):
        """Populate a table with commission data."""
        table.setRowCount(0)
        payment_repo = CommissionPaymentRepository()

        for commission in commissions:
            row = table.rowCount()
            table.insertRow(row)

            # Commission ID
            table.setItem(row, 0, QTableWidgetItem(str(commission.id)))

            # Deal ID
            table.setItem(row, 1, QTableWidgetItem(f"Deal #{commission.deal_id}"))

            # Party Type
            party_type = commission.party_type.replace('_', ' ').title()
            table.setItem(row, 2, QTableWidgetItem(party_type))

            # Party Name
            table.setItem(row, 3, QTableWidgetItem(commission.party_name or '-'))

            # Amount
            amount_str = self.format_currency(commission.commission_amount)
            table.setItem(row, 4, QTableWidgetItem(amount_str))

            # Calculate payments
            payments = payment_repo.get_by_commission_id(commission.id)
            total_received = sum(p.amount for p in payments)
            outstanding = commission.commission_amount - total_received

            # Status
            status_text = commission.status.replace('_', ' ').title()
            status_item = QTableWidgetItem(status_text)

            if commission.status == 'received':
                status_item.setForeground(Qt.darkGreen)
            elif commission.status == 'partial':
                status_item.setForeground(Qt.darkYellow)
            else:
                status_item.setForeground(Qt.red)

            table.setItem(row, 5, status_item)

            # Received
            received_item = QTableWidgetItem(self.format_currency(total_received))
            table.setItem(row, 6, received_item)

            # Outstanding
            outstanding_item = QTableWidgetItem(self.format_currency(outstanding))
            if outstanding > 0:
                outstanding_item.setForeground(Qt.red)
            table.setItem(row, 7, outstanding_item)

            # Store commission_id
            table.item(row, 0).setData(Qt.UserRole, commission.id)

    
    def view_commission_details(self, index):
        """View/edit commission details (double-click)."""
        from modules.commission.ui.commission_dialog import CommissionDialog
        
        table = self.tabs.currentWidget()
        row = index.row()
        commission_id = table.item(row, 0).data(Qt.UserRole)
        
        if not commission_id:
            return
        
        try:
            commission = self.commission_service.get_by_id(commission_id)
            if commission:
                dialog = CommissionDialog(self.commission_service, commission=commission, parent=self)
                if dialog.exec():
                    self.refresh()
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n=== ERROR in commission details ===")
            print(f"Error: {e}")
            print(f"Traceback:\n{error_details}")
            print("=" * 50)
            QMessageBox.warning(self, "Error", f"Failed to open commission:\n{str(e)}\n\nCheck console for details")
    
    def add_commission_structure(self):
        """Open add commission structure dialog."""
        from modules.commission.ui.commission_dialog import CommissionDialog
        
        dialog = CommissionDialog(self.commission_service, parent=self)
        if dialog.exec():
            self.refresh()
    
    def record_payment(self):
        """Open record payment dialog."""
        from modules.commission.ui.payment_dialog import PaymentDialog
        
        dialog = PaymentDialog(self.commission_service, parent=self)
        if dialog.exec():
            self.refresh()
    
    def apply_filters(self):
        """Apply filters to current table."""
        # For now, just refresh
        self.on_tab_changed(self.tabs.currentIndex())
    
    def on_tab_changed(self, index):
        """Handle tab change."""
        if index == 0:
            self.load_pending_commissions()
        elif index == 1:
            self.load_received_commissions()
        elif index == 2:
            self.load_all_commissions()
    
    def format_currency(self, amount):
        """Format amount as Indian currency."""
        if amount >= 10000000:  # 1 Crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"₹{amount/100000:.2f} L"
        elif amount >= 1000:
            return f"₹{amount/1000:.1f}K"
        else:
            return f"₹{amount:,.0f}"
    
    def refresh(self):
        """Refresh all data."""
        self.load_data()