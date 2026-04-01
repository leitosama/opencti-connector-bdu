"""OpenCTI BDU Connector main module"""

import traceback

from src.connector import BDUConnector

if __name__ == "__main__":
    """
    Entry point of the script
    """
    try:
        connector = BDUConnector()
        connector.run()
    except Exception:
        traceback.print_exc()
        exit(1)
