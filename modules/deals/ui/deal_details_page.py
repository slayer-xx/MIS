"""
Deal Details Page
Comprehensive view of a single deal with all related information.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QScrollArea, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QTabWidget, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from datetime import datetime


class DealDetailsPage(QWidget):
    """Detailed view of a single deal."""
    
    close_requested = Signal()
    
    def __init__(self, deal_service, deal_id, action_service=None, commission_service=None, parent=None):
        super().__init__(parent)
        self.deal_service = deal_service
        self.deal_id = deal_id
        self.action_service = action_service
        self.commission_service = commission_service
        self.deal = None
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the deal details UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header with back button
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back to Deals")
        back_btn.clicked.connect(self.close_requested.emit)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        
        # Edit button
        edit_btn = QPushButton("✏️ Edit Deal")
        edit_btn.setObjectName("primaryButton")
        edit_btn.clicked.connect(self.edit_deal)
        header_layout.addWidget(edit_btn)
        
        layout.addLayout(header_layout)
        
        # Title
        self.title_label = QLabel("Deal Details")
        self.title_label.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        
        # Deal Information Section
        self.info_frame = self.create_info_section()
        container_layout.addWidget(self.info_frame)
        
        # Tabs for related data
        self.tabs = QTabWidget()
        
        # Actions tab
        self.actions_tab = self.create_actions_tab()
        self.tabs.addTab(self.actions_tab, "📋 Actions")
        
        # Commission tab
        self.commission_tab = self.create_commission_tab()
        self.tabs.addTab(self.commission_tab, "💰 Commission")
        
        # Notes tab
        self.notes_tab = self.create_notes_tab()
        self.tabs.addTab(self.notes_tab, "📝 Notes")
        
        container_layout.addWidget(self.tabs)
        
        container.setLayout(container_layout)
        scroll.setWidget(container)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def create_info_section(self):
        """Create deal information section."""
        frame = QFrame()
        frame.setObjectName("cardFrame")
        frame.setFrameShape(QFrame.Box)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Section title
        title = QLabel("📊 Deal Information")
        title.setObjectName("sectionTitle")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Grid for details
        self.info_grid = QGridLayout()
        self.info_grid.setSpacing(10)
        
        # Placeholder labels (will be filled in load_data)
        self.deal_type_label = QLabel("")
        self.status_label = QLabel("")
        self.client_label = QLabel("")
        self.property_label = QLabel("")
        self.value_label = QLabel("")
        self.commission_label = QLabel("")
        self.created_label = QLabel("")
        
        self.info_grid.addWidget(QLabel("<b>Deal Type:</b>"), 0, 0)
        self.info_grid.addWidget(self.deal_type_label, 0, 1)
        
        self.info_grid.addWidget(QLabel("<b>Status:</b>"), 0, 2)
        self.info_grid.addWidget(self.status_label, 0, 3)
        
        self.info_grid.addWidget(QLabel("<b>Client:</b>"), 1, 0)
        self.info_grid.addWidget(self.client_label, 1, 1)
        
        self.info_grid.addWidget(QLabel("<b>Property:</b>"), 1, 2)
        self.info_grid.addWidget(self.property_label, 1, 3)
        
        self.info_grid.addWidget(QLabel("<b>Property Value:</b>"), 2, 0)
        self.info_grid.addWidget(self.value_label, 2, 1)
        
        self.info_grid.addWidget(QLabel("<b>Expected Commission:</b>"), 2, 2)
        self.info_grid.addWidget(self.commission_label, 2, 3)
        
        self.info_grid.addWidget(QLabel("<b>Created:</b>"), 3, 0)
        self.info_grid.addWidget(self.created_label, 3, 1)
        
        layout.addLayout(self.info_grid)
        frame.setLayout(layout)
        return frame
    
    def create_actions_tab(self):
        """Create actions tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Add action button
        add_btn = QPushButton("➕ Add Action for this Deal")
        add_btn.clicked.connect(self.add_action)
        layout.addWidget(add_btn)
        
        # Actions table
        self.actions_table = QTableWidget()
        self.actions_table.setColumnCount(5)
        self.actions_table.setHorizontalHeaderLabels(["Title", "Date", "Type", "Priority", "Status"])
        self.actions_table.horizontalHeader().setStretchLastSection(True)
        self.actions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.actions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.actions_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_commission_tab(self):
        """Create commission tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Add commission button
        add_btn = QPushButton("➕ Add Commission Structure")
        add_btn.clicked.connect(self.add_commission)
        layout.addWidget(add_btn)
        
        # Commission table
        self.commission_table = QTableWidget()
        self.commission_table.setColumnCount(5)
        self.commission_table.setHorizontalHeaderLabels(["Party Type", "Party Name", "Amount", "Status", "Outstanding"])
        self.commission_table.horizontalHeader().setStretchLastSection(True)
        self.commission_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.commission_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.commission_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_notes_tab(self):
        """Create notes tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Deal notes and history will appear here")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        widget.setLayout(layout)
        return widget
    
    def load_data(self):
        """Load deal data and related information."""
        try:
            self.deal = self.deal_service.get_by_id(self.deal_id)
            if not self.deal:
                QMessageBox.warning(self, "Error", "Deal not found")
                self.close_requested.emit()
                return
            
            # Update title
            self.title_label.setText(f"Deal: {self.deal.title}")
            
            # Update info section
            self.deal_type_label.setText(self.deal.deal_type or "N/A")
            self.status_label.setText(self.deal.status or "N/A")
            self.client_label.setText(self.deal.client_name or "N/A")
            self.property_label.setText(f"{self.deal.property_type or 'N/A'} - {self.deal.property_location or 'N/A'}")
            self.value_label.setText(f"₹{self.deal.property_value:,.0f}" if self.deal.property_value else "N/A")
            self.commission_label.setText(f"₹{self.deal.expected_commission:,.0f}" if self.deal.expected_commission else "N/A")
            self.created_label.setText(self.deal.created_at.strftime("%d %b %Y") if self.deal.created_at else "N/A")
            
            # Load related data
            self.load_actions()
            self.load_commission()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load deal: {str(e)}")
    
    def load_actions(self):
        """Load actions related to this deal."""
        if not self.action_service:
            return
        
        try:
            actions = self.action_service.get_actions_for_deal(self.deal_id)
            self.actions_table.setRowCount(len(actions))
            
            for row, action in enumerate(actions):
                self.actions_table.setItem(row, 0, QTableWidgetItem(action.title))
                self.actions_table.setItem(row, 1, QTableWidgetItem(action.action_date.strftime("%d %b %Y")))
                self.actions_table.setItem(row, 2, QTableWidgetItem(action.action_type.replace('_', ' ').title()))
                self.actions_table.setItem(row, 3, QTableWidgetItem(action.priority.upper()))
                status = "Completed" if action.completed else "Pending"
                self.actions_table.setItem(row, 4, QTableWidgetItem(status))
        except Exception as e:
            print(f"Error loading actions: {e}")
    
    def load_commission(self):
        """Load commission structures for this deal."""
        if not self.commission_service:
            return
        
        try:
            commissions = self.commission_service.get_by_deal_id(self.deal_id)
            self.commission_table.setRowCount(len(commissions))
            
            for row, comm in enumerate(commissions):
                self.commission_table.setItem(row, 0, QTableWidgetItem(comm.party_type or ""))
                self.commission_table.setItem(row, 1, QTableWidgetItem(comm.party_name or ""))
                self.commission_table.setItem(row, 2, QTableWidgetItem(f"₹{comm.commission_amount:,.0f}"))
                self.commission_table.setItem(row, 3, QTableWidgetItem(comm.status or ""))
                # Calculate outstanding (simplified - would need payment data)
                self.commission_table.setItem(row, 4, QTableWidgetItem("N/A"))
        except Exception as e:
            print(f"Error loading commission: {e}")
    
    def edit_deal(self):
        """Open edit dialog for this deal."""
        from modules.deals.ui.add_deal_dialog import AddDealDialog
        
        dialog = AddDealDialog(self.deal_service, deal=self.deal, parent=self)
        if dialog.exec():
            self.load_data()
    
    def add_action(self):
        """Add a new action for this deal."""
        if not self.action_service:
            QMessageBox.information(self, "Info", "Action service not available")
            return
        
        from modules.actions.ui.action_dialog import ActionDialog
        
        dialog = ActionDialog(self.action_service, parent=self)
        # Pre-fill deal_id if the dialog supports it
        if dialog.exec():
            self.load_actions()
    
    def add_commission(self):
        """Add a new commission structure for this deal."""
        if not self.commission_service:
            QMessageBox.information(self, "Info", "Commission service not available")
            return
        
        from modules.commission.ui.commission_dialog import CommissionDialog
        
        dialog = CommissionDialog(self.commission_service, parent=self)
        # Pre-fill deal_id if the dialog supports it
        if dialog.exec():
            self.load_commission()
