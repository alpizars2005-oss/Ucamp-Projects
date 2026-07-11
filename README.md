# UCAMP Projects

A collection of projects, weekly challenges, and programming exercises completed during my training at **UCAMP**.

This repository documents my progress with Python fundamentals, programming logic, data validation, problem-solving, and version control with Git and GitHub.

> **Resumen en español:** Este repositorio reúne los proyectos y retos que he desarrollado durante mi formación en UCAMP. Los programas están escritos principalmente en español porque forman parte de actividades académicas evaluadas en ese idioma.

## Repository Structure

```text
Ucamp-Projects/
├── Proyecto_Ucamp/
│   ├── Calculadora_de_IMC.py
│   └── Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py
├── Retos_M2/
│   ├── Semana5.py
│   ├── Semana6.py
│   ├── Semana7.py
│   ├── Semana8.py
│   └── Semana9.py
└── README.md
```

## Main Projects

### Module 1 — BMI Calculator

**File:** [`Proyecto_Ucamp/Calculadora_de_IMC.py`](Proyecto_Ucamp/Calculadora_de_IMC.py)

My first Python project. The program requests the user's name, age, weight, and height, validates the entered information, calculates the Body Mass Index (BMI), and displays the corresponding classification.

Concepts practiced:

- User input with `input()`
- Numeric conversion with `float()`
- Data validation using `while`
- Error handling with `try/except`
- Conditional logic with `if`, `elif`, and `else`
- Mathematical operations and formatted output

### Module 2 — Data Validation and Operations

**File:** [`Proyecto_Ucamp/Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py`](Proyecto_Ucamp/Angel_Alfredo_Alpizar_Sanchez_proyectoM2.py)

This project contains two exercises:

1. **Word Length:** verifies whether a word contains between 4 and 8 characters and reports whether letters are missing or exceeding the limit.
2. **Cartesian Quadrant:** requests X and Y coordinates, rejects zero or non-integer values, and identifies the quadrant where the point is located.

Concepts practiced:

- String cleanup with `strip()`
- Character counting with `len()`
- Compound conditions
- Repetition with `while True`
- Input validation and `ValueError` handling
- Cartesian-plane logic
- Code comments and program organization

## Module 2 Weekly Challenges

| Week | Exercise | Main concepts | File |
|---|---|---|---|
| **5** | Calculates the difference between the current year and another year entered by the user. | Arithmetic operations, nested conditionals, absolute values | [`Semana5.py`](Retos_M2/Semana5.py) |
| **6** | Requests and confirms a password that must begin with a number, allowing a maximum of three errors. | Strings, loops, counters, validation | [`Semana6.py`](Retos_M2/Semana6.py) |
| **7** | Registers students and their grades, validates values from 0 to 10, and calculates each average. | Lists, nested loops, `try/except`, averages | [`Semana7.py`](Retos_M2/Semana7.py) |
| **8** | Finds rainbow colors in a Spanish sentence and translates them into English or French. | Dictionaries, loops, string search, language selection | [`Semana8.py`](Retos_M2/Semana8.py) |
| **9** | Displays the previous and next letters of the alphabet and includes an option to end the program. | Functions, indexes, validation, cyclic navigation, loops | [`Semana9.py`](Retos_M2/Semana9.py) |

## Technologies and Tools

- Python
- Git
- GitHub
- Visual Studio Code
- Windows and Linux

## Skills Practiced

- Variables and data types
- User input and formatted output
- Arithmetic and comparison operators
- Conditional statements
- `while` and `for` loops
- Lists and dictionaries
- Functions
- String methods
- Input validation
- Basic exception handling
- Code organization and documentation
- Version control and repository management

## Running the Programs

The exercises only require Python and do not use third-party packages.

1. Clone the repository:

   ```bash
   git clone https://github.com/alpizars2005-oss/Ucamp-Projects.git
   ```

2. Enter the repository:

   ```bash
   cd Ucamp-Projects
   ```

3. Run any exercise, for example:

   ```bash
   python Proyecto_Ucamp/Calculadora_de_IMC.py
   ```

   On some Linux systems, the command may be:

   ```bash
   python3 Proyecto_Ucamp/Calculadora_de_IMC.py
   ```

## Learning Reflection

These projects show my progress from writing my first interactive Python program to creating solutions with stronger validations, nested control structures, collections, functions, and error handling.

The bootcamp has helped me understand that programming is not only about making a program work, but also about breaking a problem into smaller steps, anticipating invalid input, organizing code clearly, and documenting the solution so that another person can understand it.

I will continue updating this repository as I complete new modules, challenges, and projects.

## Author

**Angel Alfredo Alpizar Sanchez**  
Computer Systems Engineering student and UCAMP learner.
