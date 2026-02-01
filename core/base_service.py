"""
Base Service Layer
Foundation for all module services following clean architecture.

This provides common service functionality while maintaining module independence.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseService:
    """
    Base service class providing common functionality for all modules.
    
    Design Principles:
    1. Services contain business logic
    2. Services use repositories for data access
    3. Services validate input
    4. Services format output
    5. Services are stateless
    """
    
    def __init__(self, repository):
        """
        Initialize service with its repository.
        
        Args:
            repository: The data access layer (repository) for this service
        """
        self.repository = repository
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> tuple[bool, str]:
        """
        Validate that all required fields are present and not empty.
        
        Args:
            data: Dictionary of field values
            required_fields: List of field names that are required
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"{field.replace('_', ' ').title()} is required"
        return True, ""
    
    def validate_numeric_field(self, value: Any, field_name: str, 
                              min_value: Optional[float] = None,
                              max_value: Optional[float] = None) -> tuple[bool, str]:
        """
        Validate numeric field.
        
        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            min_value: Minimum allowed value (optional)
            max_value: Maximum allowed value (optional)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value is None:
            return True, ""  # Optional field
        
        try:
            num_value = float(value)
            
            if min_value is not None and num_value < min_value:
                return False, f"{field_name} must be at least {min_value}"
            
            if max_value is not None and num_value > max_value:
                return False, f"{field_name} must not exceed {max_value}"
            
            return True, ""
        except (ValueError, TypeError):
            return False, f"{field_name} must be a valid number"
    
    def sanitize_string(self, value: Optional[str]) -> str:
        """
        Sanitize string input by stripping whitespace.
        
        Args:
            value: String to sanitize
            
        Returns:
            Sanitized string or empty string if None
        """
        if value is None:
            return ""
        return str(value).strip()
    
    def format_currency(self, amount: Optional[float], symbol: str = "₹") -> str:
        """
        Format amount as currency.
        
        Args:
            amount: Amount to format
            symbol: Currency symbol
            
        Returns:
            Formatted currency string
        """
        if amount is None:
            return f"{symbol}0.00"
        return f"{symbol}{amount:,.2f}"
    
    def format_indian_currency(self, amount: Optional[float]) -> str:
        """
        Format amount in Indian currency style (lakhs, crores).
        
        Args:
            amount: Amount to format
            
        Returns:
            Formatted currency string
        """
        if amount is None:
            return "₹0"
        
        if amount >= 10000000:  # 1 crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 lakh
            return f"₹{amount/100000:.2f} L"
        elif amount >= 1000:  # 1 thousand
            return f"₹{amount/1000:.2f} K"
        else:
            return f"₹{amount:,.2f}"
    
    def format_date(self, date_obj: Optional[datetime], format_str: str = "%d-%m-%Y") -> str:
        """
        Format datetime object as string.
        
        Args:
            date_obj: Date to format
            format_str: Format string
            
        Returns:
            Formatted date string
        """
        if date_obj is None:
            return ""
        return date_obj.strftime(format_str)
    
    def parse_date(self, date_string: str, format_str: str = "%d-%m-%Y") -> Optional[datetime]:
        """
        Parse date string to datetime object.
        
        Args:
            date_string: Date string to parse
            format_str: Expected format
            
        Returns:
            Datetime object or None if invalid
        """
        if not date_string:
            return None
        
        try:
            return datetime.strptime(date_string, format_str)
        except ValueError:
            return None
    
    def get_all(self, **filters) -> List[Any]:
        """
        Get all records with optional filters.
        
        Args:
            **filters: Filter criteria
            
        Returns:
            List of records
        """
        return self.repository.get_all(**filters)
    
    def get_by_id(self, record_id: int) -> Optional[Any]:
        """
        Get single record by ID.
        
        Args:
            record_id: ID of the record
            
        Returns:
            Record object or None
        """
        return self.repository.get_by_id(record_id)
    
    def delete(self, record_id: int) -> bool:
        """
        Delete a record.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return self.repository.delete(record_id)
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def search(self, query: str, search_fields: Optional[List[str]] = None) -> List[Any]:
        """
        Search records across specified fields.
        
        Args:
            query: Search query
            search_fields: Fields to search in (if supported by repository)
            
        Returns:
            List of matching records
        """
        if hasattr(self.repository, 'search'):
            if search_fields:
                return self.repository.search(query, search_fields)
            return self.repository.search(query)
        return []
    
    def count(self, **filters) -> int:
        """
        Count records matching filters.
        
        Args:
            **filters: Filter criteria
            
        Returns:
            Count of matching records
        """
        if hasattr(self.repository, 'count'):
            return self.repository.count(**filters)
        return len(self.get_all(**filters))
    
    def validate_phone_number(self, phone: str) -> tuple[bool, str]:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone:
            return False, "Phone number is required"
        
        # Remove common separators
        cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Check if it's all digits
        if not cleaned.isdigit():
            return False, "Phone number must contain only digits"
        
        # Check length
        if len(cleaned) < 10 or len(cleaned) > 15:
            return False, "Phone number must be between 10 and 15 digits"
        
        return True, ""
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return True, ""  # Email is optional in most cases
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    def log_action(self, action: str, details: str = ""):
        """
        Log service action (for future audit trail).
        
        Args:
            action: Action performed
            details: Additional details
        """
        # Placeholder for future logging implementation
        pass


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class BusinessRuleError(Exception):
    """Custom exception for business rule violations"""
    pass
