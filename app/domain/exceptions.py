# Excepciones de dominio (negocio)

class DomainError(Exception):
    """Base para errores de negocio."""
    pass


class EdadInvalidaError(DomainError):
    """Edad no numérica o formato inválido."""
    pass


class EdadNegativaError(DomainError):
    """Edad menor que 0."""
    pass


class LineaCorruptaError(DomainError):
    """Línea con formato incorrecto."""
    pass


class ArchivoVacioError(DomainError):
    """Archivo sin contenido."""
    pass
