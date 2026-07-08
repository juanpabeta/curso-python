CREATE TABLE estudiantes(
	id SERIAL PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL
);

CREATE TABLE cursos(
	id SERIAL PRIMARY KEY,
	nombre_curso VARCHAR(100) NOT NULL

);

CREATE TABLE inscripciones(
	id SERIAL PRIMARY KEY,
	estudiantes_id INT,
	curso_id INT,
	FOREIGN KEY(estudiantes_id) REFERENCES estudiantes(id),
	FOREIGN KEY(curso_id) REFERENCES cursos(id)


);

