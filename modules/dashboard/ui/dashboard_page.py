"""
Dashboard Page
Main dashboard showing business overview and key metrics.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class DashboardPage(QWidget):
    """Main dashboard with business overview and key metrics."""
    
    def __init__(self, dashboard_service, action_service=None):
        super().__init__()
        self.dashboard_service = dashboard_service
        self.action_service = action_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the dashboard UI."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Container widget for scroll content
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 Business Dashboard")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        container_layout.addWidget(title)
        
        # Business Overview Section
        self.overview_frame = self.create_overview_section()
        container_layout.addWidget(self.overview_frame)
        
        # Money Status Section
        self.money_frame = self.create_money_section()
        container_layout.addWidget(self.money_frame)
        
        # Add stretch at bottom
        container_layout.addStretch()
        
        container.setLayout(container_layout)
        scroll.setWidget(container)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def create_overview_section(self):
        """Create business overview section."""
        frame = QFrame()
        frame.setObjectName("cardFrame")
        frame.setFrameShape(QFrame.Box)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Section title
        title = QLabel("📈 BUSINESS OVERVIEW")
        title.setObjectName("sectionTitle")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Grid for stat cards
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Create stat cards
        self.active_deals_card = self.create_stat_card("Active Deals", "0", "💼")
        self.deals_month_card = self.create_stat_card("Deals This Month", "0", "📅")
        self.total_commission_card = self.create_stat_card("Total Expected Commission", "₹0", "💰")
        self.received_month_card = self.create_stat_card("Received This Month", "₹0", "✅")
        
        grid.addWidget(self.active_deals_card, 0, 0)
        grid.addWidget(self.deals_month_card, 0, 1)
        grid.addWidget(self.total_commission_card, 0, 2)
        grid.addWidget(self.received_month_card, 0, 3)
        
        layout.addLayout(grid)
        frame.setLayout(layout)
        return frame
    
    def create_money_section(self):
        """Create money status section."""
        frame = QFrame()
        frame.setObjectName("cardFrame")
        frame.setFrameShape(QFrame.Box)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Section title
        title = QLabel("💰 FINANCIAL STATUS")
        title.setObjectName("sectionTitle")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Grid for money cards
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Create money cards
        self.pending_commission_card = self.create_stat_card("Pending Commission", "₹0", "⏳")
        self.total_expected_card = self.create_stat_card("Total Expected", "₹0", "📊")
        self.total_received_card = self.create_stat_card("Total Received", "₹0", "💵")
        self.outstanding_card = self.create_stat_card("Outstanding", "₹0", "📌")
        self.month_expenses_card = self.create_stat_card("Month Expenses", "₹0", "💸")
        
        grid.addWidget(self.pending_commission_card, 0, 0)
        grid.addWidget(self.total_expected_card, 0, 1)
        grid.addWidget(self.total_received_card, 0, 2)
        grid.addWidget(self.outstanding_card, 1, 0)
        grid.addWidget(self.month_expenses_card, 1, 1)
        
        layout.addLayout(grid)
        frame.setLayout(layout)
        return frame
    
    def create_stat_card(self, title_text, value_text, icon):
        """Create a stat card widget."""
        card = QFrame()
        card.setObjectName("statCard")
        card.setFrameShape(QFrame.Box)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        # Icon and title row
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_font = QFont()
        icon_font.setPointSize(16)
        icon_label.setFont(icon_font)
        top_layout.addWidget(icon_label)
        
        title = QLabel(title_text)
        title.setObjectName("statTitle")
        title_font = QFont()
        title_font.setPointSize(9)
        title.setFont(title_font)
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Value
        value = QLabel(value_text)
        value.setObjectName("statValue")
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value.setFont(value_font)
        layout.addWidget(value)
        
        card.setLayout(layout)
        return card
    
    def load_data(self):
        """Load dashboard data."""
        try:
            summary = self.dashboard_service.get_dashboard_summary()
            
            # Update business overview
            self.update_card_value(self.active_deals_card, str(summary.get('active_deals', 0)))
            self.update_card_value(self.deals_month_card, str(summary.get('deals_this_month', 0)))
            self.update_card_value(self.total_commission_card, f"₹{summary.get('total_expected_commission', 0):,.0f}")
            self.update_card_value(self.received_month_card, f"₹{summary.get('received_this_month', 0):,.0f}")
            
            # Update money section
            self.update_card_value(self.pending_commission_card, f"₹{summary.get('pending_commission', 0):,.0f}")
            self.update_card_value(self.total_expected_card, f"₹{summary.get('total_expected', 0):,.0f}")
            self.update_card_value(self.total_received_card, f"₹{summary.get('total_received', 0):,.0f}")
            self.update_card_value(self.outstanding_card, f"₹{summary.get('outstanding', 0):,.0f}")
            self.update_card_value(self.month_expenses_card, f"₹{summary.get('month_expenses', 0):,.0f}")
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def update_card_value(self, card, value_text):
        """Update the value in a stat card."""
        # Find the value label (second label in the card, which is the statValue)
        value_label = card.findChild(QLabel, "statValue")
        if value_label:
            value_label.setText(value_text)
    
    def refresh(self):
        """Refresh dashboard data."""
        self.load_data()
