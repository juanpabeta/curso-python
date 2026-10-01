"""Contratos ejecutables para capacidades solicitadas que aún no existen."""

import pytest
from fastapi.testclient import TestClient

pytestmark = [pytest.mark.e2e, pytest.mark.contract]


@pytest.mark.xfail(
    strict=True,
    reason="No existe un dominio ni endpoint de pagos en el producto actual",
)
def test_student_pays_enrollment(api_client: TestClient) -> None:
    response = api_client.post(
        "/payments/",
        json={"enrollment_id": 1, "amount": "250.00", "currency": "COP"},
    )
    assert response.status_code == 201


@pytest.mark.xfail(
    strict=True,
    reason="No existe un dominio ni endpoint de certificados en el producto actual",
)
def test_student_generates_certificate(api_client: TestClient) -> None:
    response = api_client.post("/certificates/", json={"enrollment_id": 1})
    assert response.status_code == 201


@pytest.mark.xfail(
    strict=True,
    reason="No existe un dominio ni endpoint de reportes en el producto actual",
)
def test_admin_generates_academic_report(api_client: TestClient) -> None:
    response = api_client.get("/reports/academic?period_id=1")
    assert response.status_code == 200
