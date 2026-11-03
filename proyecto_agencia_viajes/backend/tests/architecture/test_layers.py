import ast
from pathlib import Path


ROOT = Path(__file__).parents[2] / "app"
MODULES = ("auth", "users", "clients", "inquiries", "interactions", "reminders", "reports")


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    return imports


def test_modules_have_flat_layout():
    for module in MODULES:
        module_path = ROOT / module
        assert not any(
            (module_path / old).exists()
            for old in ("domain", "application", "infrastructure", "presentation")
        )


def test_orm_models_are_in_models_and_schemas_are_pydantic_only():
    for module in MODULES:
        models = ROOT / module / "models.py"
        schemas = ROOT / module / "schemas.py"
        if not models.exists():
            continue
        assert "sqlalchemy" in " ".join(_imports(models))
        if schemas.exists():
            assert "sqlalchemy" not in " ".join(_imports(schemas))


def test_core_does_not_import_business_modules():
    for path in (ROOT / "core").glob("*.py"):
        assert not any(imported.startswith("app.") and imported.split(".")[1] != "core" for imported in _imports(path)), path


def test_ports_import_only_their_own_models():
    for module in MODULES:
        path = ROOT / module / "ports.py"
        if not path.exists():
            continue
        for imported in _imports(path):
            if imported.startswith("app."):
                assert imported == f"app.{module}.models", path


def test_services_can_use_models_but_not_outer_layers():
    forbidden = (".repository", ".routes", ".schemas")
    for module in MODULES:
        path = ROOT / module / "services.py"
        if path.exists():
            assert not any(any(item in imported for item in forbidden) for imported in _imports(path)), path


def test_routes_and_schemas_do_not_import_repositories():
    for module in MODULES:
        for name in ("routes.py", "schemas.py"):
            path = ROOT / module / name
            if path.exists():
                assert not any(".repository" in imported for imported in _imports(path)), path


def test_only_composition_files_import_repositories():
    for path in ROOT.rglob("*.py"):
        if path.name in {"repository.py", "container.py", "main.py"}:
            continue
        assert ".repository" not in " ".join(_imports(path)), path
