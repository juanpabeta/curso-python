import csv
from pathlib import Path
from typing import List, Dict

class CSVManager:
    
    def __init__(self, path: str, delimiter: str = ",") -> None:
        self._path = Path(path)
        self._delimiter = delimiter
        self._path.touch(exist_ok=True)
    
    def read_all(self) -> List[Dict]:
        
        with self._path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, delimiter=self._delimiter)
            return list(reader)
    
    def write_all(self, rows: List[Dict], headers: List[str]) -> None:
        
        with self._path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter=self._delimiter)
            writer.writeheader()
            writer.writerows(rows)
        
        