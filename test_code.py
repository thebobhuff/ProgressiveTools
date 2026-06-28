# test_code.py
"""
Sample Module for Testing JIT Agent Progressive Disclosure System.
"""

class DatabaseConnection:
    """
    Manages connections to the test database.
    """
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        # Missing docstring!
        self.connected = True
        print(f"Connected to database at {self.host}:{self.port}")
        return True

def calculate_checksum(data: str) -> str:
    # Missing docstring!
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()
