class DomainError(Exception):
    pass

class EdadInvalidaError(DomainError):
    pass

class EdadNegativaError(DomainError):
    pass

class LineaCorruptaError(DomainError):
    pass

class ArchivoVacioError(DomainError):
    pass