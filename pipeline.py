"""
ETL used for data ingestion and tracking new Census
Bureau API releases.

Executes biweekly.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from ingestion._functions import ingestion



def main():
    ingestion()


if __name__ == '__main__':
    main()