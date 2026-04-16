from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePOSAdapter(ABC):
    """
    Abstract base class for all POS integrations.
    Any new POS integration MUST implement these methods.
    """
    
    @abstractmethod
    def push_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Push order to the external POS.
        Must return a dict containing at least {"success": bool}.
        """
        pass
