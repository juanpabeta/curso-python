## Casos de uso para `main.py`

**Dónde crear el archivo de datos**

Crea el archivo `usuarios.csv` **en la raíz del proyecto**, es decir, en la misma carpeta donde está `main.py`:

- Ruta del proyecto: `app/`
- Ruta del archivo: `app/usuarios.csv`


El archivo CSV debe tener una cabecera con al menos estas columnas:

```text
nombre,edad
```

Después de configurar el archivo, ejecuta:

```bash
python main.py
```

---

### 1. Caso feliz (todo OK)

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan,30
Ana,25
Luis,40
```

**Resultado esperado**
- Se muestran los usuarios cargados correctamente.
- No aparece ningún mensaje de error.
- Se imprime `Proceso finalizado.` al final.

---

### 2. Archivo no encontrado

**Acción**
- Borrar o renombrar `usuarios.csv` para que no exista cuando se ejecute el programa (o ejecutar desde otra carpeta sin tener el archivo en `app/`).

**Resultado esperado**
- Mensaje: `[ERROR SISTEMA] El archivo no existe.`
- Se imprime `Proceso finalizado.` al final.

---

### 3. Permiso denegado

En Windows es un poco difícil simular un error de permisos “de verdad”.

- **Opción A:** intentar leer un archivo en una carpeta del sistema donde normalmente no tienes permisos de escritura/lectura.
  1. Abre `main.py`.
  2. Cambia la línea donde se crea el repositorio:
     
     ```python
     repo = FileRepository("usuarios.csv")
     ```
     
     por algo como:
     
     ```python
     repo = FileRepository("C:\\Windows\\System32\\archivo_que_no_existe.csv")
     ```
  3. Guarda el archivo.
  4. Ejecuta de nuevo `python main.py`.
  5. Según la configuración del equipo, puede que se obtenga `PermissionError` o `FileNotFoundError`.

- **Opción B:** en sistemas multiusuario (servidores, Linux, etc.) es habitual que ciertos archivos/carpetas no puedan ser leídos por todos los usuarios; cuando el programa intenta abrirlos, se lanza `PermissionError`. En Windows doméstico esto es menos frecuente.

**Resultado esperado**
- Si se produce realmente un `PermissionError`, verás un mensaje: `[ERROR PERMISOS] ...`
- En cualquier caso, después se imprime `Proceso finalizado.` al final.

---

### 4. Archivo vacío / sin filas de datos

**Contenido de `usuarios.csv`:**

```text
nombre,edad
```

(solo cabecera, sin filas de usuarios)

**Resultado esperado**
- Mensaje: `[ERROR DATOS] El archivo no contiene usuarios.`
- Se imprime `Proceso finalizado.` al final.

---

### 5. Línea corrupta (faltan columnas)

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan
Ana,25
```

**Resultado esperado**
- Mensaje: `[ERROR FORMATO] Línea corrupta en línea 2`
- Se imprime `Proceso finalizado.` al final.

---

### 6. Edad no válida (no numérica)

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan,treinta
Ana,25
```

**Resultado esperado**
- Mensaje: `[ERROR VALIDACIÓN] Edad inválida en línea 2`
- Se imprime `Proceso finalizado.` al final.

---

### 7. Edad negativa (regla de negocio)

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan,-5
Ana,25
```

**Resultado esperado**
- Mensaje: `[ERROR NEGOCIO] La edad no puede ser negativa.`
- Se imprime `Proceso finalizado.` al final.

---

### 8. Varias líneas corruptas

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan,30
SinComaNiEdad
Ana,25
```

**Resultado esperado**
- Mensaje: `[ERROR FORMATO] Línea corrupta en línea 3`
- Se imprime `Proceso finalizado.` al final.

---

### 9. Campos vacíos

**Contenido de `usuarios.csv`:**

```text
nombre,edad
Juan,
,25
```

**Resultado esperado**
- Mensaje: `[ERROR FORMATO] Línea corrupta en línea 2` (o 3, según qué línea se procese primero con error).
- Se imprime `Proceso finalizado.` al final.

---

### 10. Problema de encoding (no UTF-8)

**Acción**
- Crear `usuarios.csv` guardándolo con otro encoding (por ejemplo ISO-8859-1) y con caracteres especiales, manteniendo en el código la lectura como `encoding="utf-8"`.

**Resultado esperado**
- Mensaje: `[ERROR ENCODING] El archivo no está en UTF-8.`
- Se imprime `Proceso finalizado.` al final.
