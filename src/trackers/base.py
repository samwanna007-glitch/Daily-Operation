from abc import ABC, abstractmethod


class BaseTracker(ABC):
    """Abstract base class for all trackers."""

    def __init__(self, database_id, data_path, log_path="logs/tracker.log"):
        self.database_id = database_id
        self.data_path = data_path
        self.log_path = log_path

    @abstractmethod
    def fetch_items(self):
        """Fetch items from the source. Returns list of item dicts."""
        pass

    @abstractmethod
    def fetch_items(self):
        """Fetch items from the source. Returns list of item dicts."""
        pass