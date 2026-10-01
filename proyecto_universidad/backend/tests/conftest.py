"""Registro central de plugins de fixtures.

Todos los fixtures tienen scope=function para garantizar aislamiento. Un scope
session solo sería apropiado para recursos inmutables costosos (por ejemplo,
una imagen de contenedor); las sesiones y los datos nunca deben compartirse.
"""

pytest_plugins = (
    "tests.fixtures.database",
    "tests.fixtures.api",
)
