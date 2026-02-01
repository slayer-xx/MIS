"""
Actions List Page
View and manage all actions with filtering by status and type.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QTabWidget, QComboBox,
    QLineEdit, QCheckBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from datetime import datetime


class ActionsListPage(QWidget):
    """Actions list page with tabs and filtering."""
    
    action_selected = Signal(int)
    
    def __init__(self, action_service):
        super().__init__()
        self.action_service = action_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the actions list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 Actions & Follow-ups")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add action button
        add_btn = QPushButton("➕ Add New Action")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_action)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Type filter
        type_label = QLabel("Type:")
        filter_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "call", "meeting", "site_visit", "follow_up", "documentation", "other"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)
        
        # Priority filter
        priority_label = QLabel("Priority:")
        filter_layout.addWidget(priority_label)
        
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "low", "medium", "high"])
        self.priority_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.priority_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search actions...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Today tab
        self.today_table = self.create_actions_table()
        self.tabs.addTab(self.today_table, "📅 Today")
        
        # Upcoming tab
        self.upcoming_table = self.create_actions_table()
        self.tabs.addTab(self.upcoming_table, "📆 Upcoming")
        
        # Overdue tab
        self.overdue_table = self.create_actions_table()
        self.tabs.addTab(self.overdue_table, "⚠️ Overdue")
        
        # All tab
        self.all_table = self.create_actions_table()
        self.tabs.addTab(self.all_table, "📋 All")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def create_actions_table(self):
        """Create an actions table widget."""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "✓", "Title", "Date", "Time", "Type", "Priority", "Status"
        ])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        # Column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Checkbox
        table.setColumnWidth(0, 40)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Time
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Priority
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Status
        
        # Double click to view details
        table.doubleClicked.connect(self.view_action_details)
        
        return table
    
    def load_data(self):
        """Load actions data."""
        self.load_today_actions()
        self.load_upcoming_actions()
        self.load_overdue_actions()
        self.load_all_actions()
    
    def load_today_actions(self):
        """Load today's actions."""
        try:
            actions = self.action_service.get_today_actions()
            self.populate_table(self.today_table, actions)
            
            # Update tab title with count
            count = len(actions)
            self.tabs.setTabText(0, f"📅 Today ({count})")
            
        except Exception as e:
            print(f"Error loading today's actions: {e}")
    
    def load_upcoming_actions(self):
        """Load upcoming week's actions."""
        try:
            actions = self.action_service.get_upcoming_week_actions()
            self.populate_table(self.upcoming_table, actions)
            
            # Update tab title with count
            count = len(actions)
            self.tabs.setTabText(1, f"📆 Upcoming ({count})")
            
        except Exception as e:
            print(f"Error loading upcoming actions: {e}")
    
    def load_overdue_actions(self):
        """Load overdue actions."""
        try:
            actions = self.action_service.get_overdue_actions()
            self.populate_table(self.overdue_table, actions)
            
            # Update tab title with count
            count = len(actions)
            self.tabs.setTabText(2, f"⚠️ Overdue ({count})")
            
        except Exception as e:
            print(f"Error loading overdue actions: {e}")
    
    def load_all_actions(self):
        """Load all actions."""
        try:
            actions = self.action_service.get_all()
            self.populate_table(self.all_table, actions)
            
            # Update tab title with count
            count = len(actions)
            self.tabs.setTabText(3, f"📋 All ({count})")
            
        except Exception as e:
            print(f"Error loading all actions: {e}")
    
    def populate_table(self, table, actions):
        """Populate a table with actions data."""
        table.setRowCount(0)
        
        for action in actions:
            row = table.rowCount()
            table.insertRow(row)
            
            # Checkbox for completion
            checkbox = QCheckBox()
            checkbox.setChecked(action.completed)
            checkbox.toggled.connect(
                lambda checked, aid=action.id: self.toggle_action_complete(aid, checked)
            )
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_widget.setLayout(checkbox_layout)
            table.setCellWidget(row, 0, checkbox_widget)
            
            # Title (store action ID for double-click)
            title_item = QTableWidgetItem(action.title)
            title_item.setData(Qt.UserRole, action.id)
            if action.completed:
                font = title_item.font()
                font.setStrikeOut(True)
                title_item.setFont(font)
            table.setItem(row, 1, title_item)
            
            # Date - handle both date objects and strings
            if isinstance(action.action_date, str):
                from datetime import datetime as dt
                try:
                    date_obj = dt.strptime(action.action_date, '%Y-%m-%d').date()
                    date_str = date_obj.strftime('%d %b %Y')
                except:
                    date_str = action.action_date
            else:
                date_str = action.action_date.strftime('%d %b %Y')
            table.setItem(row, 2, QTableWidgetItem(date_str))
            
            # Time
            time_str = action.action_time if action.action_time else '-'
            table.setItem(row, 3, QTableWidgetItem(time_str))
            
            # Type
            type_item = QTableWidgetItem(action.action_type.replace('_', ' ').title())
            table.setItem(row, 4, type_item)
            
            # Priority
            priority_item = QTableWidgetItem(action.priority.upper())
            if action.priority == 'high':
                priority_item.setForeground(Qt.red)
            elif action.priority == 'medium':
                priority_item.setForeground(Qt.darkYellow)
            table.setItem(row, 5, priority_item)
            
            # Status
            status_text = "Completed" if action.completed else "Pending"
            status_item = QTableWidgetItem(status_text)

            if action.completed:
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setForeground(Qt.darkYellow)

            # Store action_id in row
            table.setItem(row, 6, status_item)
    
    def toggle_action_complete(self, action_id, completed):
        try:
            if completed:
                self.action_service.mark_complete(action_id)
            else:
                self.action_service.mark_pending(action_id)

            # Reload ALL tabs so status moves between Today/Upcoming/Overdue
            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update action: {str(e)}")

    
    def view_action_details(self, index):
        """Open edit dialog for the selected action."""
        from modules.actions.ui.action_dialog import ActionDialog
        
        table = self.tabs.currentWidget()
        row = index.row()

        item = table.item(row, 1)
        if not item:
            return

        action_id = item.data(Qt.UserRole)
        if not action_id:
            return
        
        try:
            action = self.action_service.get_by_id(action_id)
            if action:
                dialog = ActionDialog(self.action_service, action=action, parent=self)
                if dialog.exec():
                    self.refresh()
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n=== ERROR in action details ===")
            print(f"Error: {e}")
            print(f"Traceback:\n{error_details}")
            print("=" * 50)
            QMessageBox.warning(self, "Error", f"Failed to open action:\n{str(e)}\n\nCheck console for details")

    
    def add_action(self):
        """Open add action dialog."""
        from modules.actions.ui.action_dialog import ActionDialog
        
        dialog = ActionDialog(self.action_service, parent=self)
        if dialog.exec():
            self.refresh()
    
    def apply_filters(self):
        """Apply filters to current table."""
        # For now, just refresh
        self.on_tab_changed(self.tabs.currentIndex())
    
    def on_tab_changed(self, index):
        """Handle tab change."""
        if index == 0:
            self.load_today_actions()
        elif index == 1:
            self.load_upcoming_actions()
        elif index == 2:
            self.load_overdue_actions()
        elif index == 3:
            self.load_all_actions()
    
    def refresh(self):
        """Refresh all data."""
        self.load_data()
