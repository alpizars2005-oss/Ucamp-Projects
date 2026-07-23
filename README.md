# Proyectos UCAMP

Repositorio con proyectos, retos semanales y ejercicios de programación realizados durante mi formación en **UCAMP**.

Este espacio documenta mi progreso en fundamentos de Python, lógica de programación, validación de datos, resolución de problemas y control de versiones con Git y GitHub.

## Idioma del repositorio

El contenido de este repositorio está escrito principalmente en **español**, ya que las actividades, instrucciones y evaluaciones del bootcamp se realizan en este idioma.

## Estructura del repositorio

```text
Ucamp-Projects/
├── Proyecto_Ucamp/
│   ├── Calculadora_de_IMC.py
│   └── Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py
├── Retos_M2/
│   ├── Semana5.py
│   ├── Semana6.py
│   ├── Semana7.py
│   └── Semana8.py
├── Retos_M3/
│   ├── Semana9.py
│   ├── Semana10.py
│   ├── README.md
│   └── Semana11/
│       ├── main.py
│       └── m_retosemanal.py
└── README.md
```

## Proyectos principales

### Módulo 1 — Calculadora de IMC

**Archivo:** [`Proyecto_Ucamp/Calculadora_de_IMC.py`](Proyecto_Ucamp/Calculadora_de_IMC.py)

Mi primer proyecto en Python. El programa solicita el nombre, edad, peso y estatura del usuario, valida la información ingresada, calcula el Índice de Masa Corporal (IMC) y muestra la clasificación correspondiente.

Conceptos practicados:

- Entrada de datos con `input()`
- Conversión numérica con `float()`
- Validación de datos mediante ciclos `while`
- Manejo de errores con `try/except`
- Condicionales `if`, `elif` y `else`
- Operaciones matemáticas y presentación de resultados

### Módulo 2 — Validación y operaciones de datos

**Archivo:** [`Proyecto_Ucamp/Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py`](Proyecto_Ucamp/Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py)

Este proyecto contiene la solución de dos ejercicios:

1. **Longitud de una palabra:** verifica si una palabra contiene entre 4 y 8 caracteres e indica si faltan o sobran letras.
2. **Encuentra el cuadrante:** solicita las coordenadas X y Y, rechaza valores iguales a cero o datos que no sean números enteros e identifica el cuadrante en el que se encuentra el punto.

Conceptos practicados:

- Limpieza de cadenas con `strip()`
- Conteo de caracteres con `len()`
- Condiciones compuestas
- Repetición con `while True`
- Validación de entradas y manejo de `ValueError`
- Lógica del plano cartesiano
- Comentarios y organización del código

## Retos semanales del Módulo 2

| Semana | Ejercicio | Conceptos principales | Archivo |
|---|---|---|---|
| **5** | Calcula la diferencia entre el año actual y otro año ingresado por el usuario. | Operaciones aritméticas, condicionales anidados y valores absolutos | [`Semana5.py`](Retos_M2/Semana5.py) |
| **6** | Solicita y confirma una contraseña que debe comenzar con un número, permitiendo un máximo de tres errores. | Cadenas, ciclos, contadores y validación | [`Semana6.py`](Retos_M2/Semana6.py) |
| **7** | Registra alumnos y calificaciones, valida valores entre 0 y 10 y calcula el promedio de cada alumno. | Listas, ciclos anidados, `try/except` y promedios | [`Semana7.py`](Retos_M2/Semana7.py) |
| **8** | Identifica colores del arcoíris dentro de una oración en español y los traduce al inglés o francés. | Diccionarios, ciclos, búsqueda en cadenas y selección de idioma | [`Semana8.py`](Retos_M2/Semana8.py) |

## Retos semanales del Módulo 3

El Módulo 3 se enfoca en funciones, módulos y organización de programas. Los retos están documentados también en [`Retos_M3/README.md`](Retos_M3/README.md).

| Semana | Ejercicio | Conceptos principales | Archivo |
|---|---|---|---|
| **9** | Muestra la letra anterior y la siguiente dentro del alfabeto e incluye una opción para finalizar el programa. | Funciones, índices, validación, navegación cíclica y ciclos | [`Semana9.py`](Retos_M3/Semana9.py) |
| **10** | Crea dos listas y elimina de la primera los elementos que también aparecen en la segunda. | Funciones, listas, conjuntos, valores de retorno y comparación de cadenas | [`Semana10.py`](Retos_M3/Semana10.py) |
| **11** | Crea varias listas y elimina de cada una los elementos que aparecen en listas posteriores. | Lista de listas, funciones, módulos, importaciones y conjuntos | [`Semana11`](Retos_M3/Semana11/) |

## Tecnologías y herramientas

- Python
- Git
- GitHub
- Visual Studio Code
- Windows y Linux

## Habilidades practicadas

- Variables y tipos de datos
- Entrada de datos y salida con formato
- Operadores aritméticos y de comparación
- Estructuras condicionales
- Ciclos `while` y `for`
- Listas, diccionarios y conjuntos
- Funciones, parámetros y valores de retorno
- Creación e importación de módulos
- Métodos de cadenas
- Validación de datos
- Manejo básico de excepciones
- Organización y documentación del código
- Control de versiones y administración de repositorios

## Cómo ejecutar los programas

Los ejercicios solamente requieren Python y no utilizan paquetes externos.

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/alpizars2005-oss/Ucamp-Projects.git
   ```

2. Entrar a la carpeta del repositorio:

   ```bash
   cd Ucamp-Projects
   ```

3. Ejecutar cualquiera de los programas, por ejemplo:

   ```bash
   python Retos_M3/Semana11/main.py
   ```

   En algunos sistemas Linux puede ser necesario utilizar:

   ```bash
   python3 Retos_M3/Semana11/main.py
   ```

## Reflexión de aprendizaje

Estos proyectos muestran mi progreso desde la creación de mi primer programa interactivo en Python hasta el desarrollo de soluciones con validaciones más completas, estructuras de control, colecciones, funciones y programas organizados en módulos.

El bootcamp me ha ayudado a comprender que programar no consiste únicamente en lograr que un programa funcione, sino también en dividir un problema en pasos más pequeños, anticipar entradas incorrectas, organizar el código de forma clara y documentar la solución para que otras personas puedan entenderla.

Continuaré actualizando este repositorio conforme complete nuevos módulos, retos y proyectos.

## Autor

**Angel Alfredo Alpizar Sanchez**  
Estudiante de Ingeniería en Sistemas Computacionales y alumno de UCAMP.
