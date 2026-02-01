"""
Deals List Page
Main page displaying all deals in a table view.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from modules.deals.services.deal_service import DealService
from modules.deals.ui.add_deal_dialog import AddDealDialog


class DealsListPage(QWidget):
    """
    Page displaying list of all deals.
    Allows adding new deals and opening deal details.
    """
    
    deal_selected = Signal(int)  # Emits deal ID when a deal is double-clicked

    def __init__(self, deal_service):
        super().__init__()
        self.service = deal_service
        self.setup_ui()
        self.load_deals()

    def setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Page title
        title_label = QLabel("Deals Management")
        title_label.setProperty("cssClass", "page-title")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Add Deal button
        add_button = QPushButton("+ Add New Deal")
        add_button.clicked.connect(self.open_add_deal_dialog)
        header_layout.addWidget(add_button)
        
        layout.addLayout(header_layout)
        
        # Table for deals
        self.deals_table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.deals_table)
        
        self.setLayout(layout)

    def setup_table(self):
        """Configure the deals table."""
        # Define columns
        columns = [
            "ID",
            "Deal Title",
            "Deal Type",
            "Status",
            "Client Name",
            "Property Value",
            "Expected Commission",
            "Created At"
        ]
        
        self.deals_table.setColumnCount(len(columns))
        self.deals_table.setHorizontalHeaderLabels(columns)
        
        # Configure table properties
        self.deals_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.deals_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.deals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.deals_table.setAlternatingRowColors(True)
        
        # Set column widths
        header = self.deals_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Title
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Client
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Value
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Commission
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Created
        
        # Connect double-click signal
        self.deals_table.doubleClicked.connect(self.on_deal_double_clicked)

    def load_deals(self):
        """Load all deals into the table."""
        try:
            deals = self.service.get_all_deals(sort_by="created_at", ascending=False)
            
            self.deals_table.setRowCount(len(deals))
            
            for row, deal in enumerate(deals):
                # ID
                id_item = QTableWidgetItem(str(deal.id))
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.deals_table.setItem(row, 0, id_item)
                
                # Title
                self.deals_table.setItem(row, 1, QTableWidgetItem(deal.title))
                
                # Deal Type
                type_item = QTableWidgetItem(deal.deal_type)
                type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.deals_table.setItem(row, 2, type_item)
                
                # Status
                status_item = QTableWidgetItem(deal.status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.deals_table.setItem(row, 3, status_item)
                
                # Client Name
                self.deals_table.setItem(row, 4, QTableWidgetItem(deal.client_name))
                
                # Property Value
                value_text = self.service.format_currency(deal.property_value)
                value_item = QTableWidgetItem(value_text)
                value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.deals_table.setItem(row, 5, value_item)
                
                # Expected Commission
                commission_text = self.service.format_currency(deal.expected_commission)
                commission_item = QTableWidgetItem(commission_text)
                commission_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.deals_table.setItem(row, 6, commission_item)
                
                # Created At
                created_text = deal.created_at.strftime("%d %b %Y")
                created_item = QTableWidgetItem(created_text)
                created_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.deals_table.setItem(row, 7, created_item)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load deals: {str(e)}"
            )

    def open_add_deal_dialog(self):
        dialog = AddDealDialog(self.service, self)
        dialog.deal_created.connect(self.load_deals)
        dialog.exec()

    def on_deal_double_clicked(self):
        """Handle double-click on a deal row."""
        current_row = self.deals_table.currentRow()
        if current_row >= 0:
            deal_id_item = self.deals_table.item(current_row, 0)
            if deal_id_item:
                deal_id = int(deal_id_item.text())
                self.deal_selected.emit(deal_id)

    def refresh(self):
        """Refresh the deals table."""
        self.load_deals()
