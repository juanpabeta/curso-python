from typing import Protocol


class MonthlyReportReader(Protocol):
    def monthly(self): ...


class ConversionReportReader(Protocol):
    def conversion(self): ...


class InactiveClientsReportReader(Protocol):
    def inactive_clients(self): ...
