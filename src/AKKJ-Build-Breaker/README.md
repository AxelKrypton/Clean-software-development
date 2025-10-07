# SU(2) Matrix Operations

The `su2.cpp` file implements the `SU2_mat` class for handling SU(2) matrices.

---

## Matrix Representation

An SU(2) matrix `U` is represented by four real numbers `(c0, c1, c2, c3)` forming a 2x2 complex matrix:

```
[  c0 + i*c1     c2 + i*c3 ]
U = [ -c2 + i*c3    c0 - i*c1 ]
```

For `U` to be a special unitary matrix, its determinant must be 1:
```
det(U) = c0^2 + c1^2 + c2^2 + c3^2
```
Thus, the condition `c0^2 + c1^2 + c2^2 + c3^2 = 1` must hold.

---

## Implemented Operations in `su2.cpp`

The `SU2_mat` class provides the following operations:

### Constructors
- Default, copy, and from components `(c0, c1, c2, c3)`.

### Addition/Subtraction (`+`, `-`)
- Performed component-wise on `(c0, c1, c2, c3)`.

### Multiplication (`*`)
- Defined for two `SU2_mat` objects, `a` and `b`, as:
    ```cpp
    res_c0 = a.c0*b.c0 - a.c1*b.c1 - a.c2*b.c2 - a.c3*b.c3;
    res_c1 = a.c0*b.c1 + a.c1*b.c0 - a.c2*b.c3 + a.c3*b.c2;
    res_c2 = a.c0*b.c2 + a.c1*b.c3 + a.c2*b.c0 - a.c3*b.c1;
    res_c3 = a.c0*b.c3 - a.c1*b.c2 + a.c2*b.c1 + a.c3*b.c0;
    ```
    **Note**: This does not correspond to standard matrix multiplication.

### Hermitian Conjugate (`dag()`)
- Transforms `(c0, c1, c2, c3)` to `(c0, -c1, -c2, -c3)`.

### Trace (`trace()`)
- Returns `2*c0`.

### Determinant (`det()`)
- Returns `c0^2 + c1^2 + c2^2 + c3^2`.

### Projection (`project_to_sun()`)
- Normalizes the matrix to have determinant 1 by dividing all components by `sqrt(det)`.

---

## Running This Project on Windows 11

### Setting Up CMake and GCC

Follow these steps to set up a **CMake + GCC (MinGW)** build environment on **Windows 11**.

---

### 1. Install CMake

Open **PowerShell** and run:

```powershell
winget install Kitware.CMake
```
After installation, verify that it works:
```powershell
cmake --version
```
If you see a version number, CMake is correctly installed.

### 2. Install MSYS2 (for GCC and Make)

MSYS2 provides a Linux-like environment and the GCC compiler toolchain for Windows.

Install it using:
```powershell
winget install MSYS2.MSYS2
```

Then open the MSYS2 MinGW 64-bit terminal (MSYS2MINGW64) from the Windows Start Menu.

### 3. Update MSYS2 and install the compiler

Inside the MSYS2 MinGW 64-bit terminal, run the following commands:
```bash
pacman -Syu
# If prompted, restart the terminal and run again:
pacman -Syu
pacman -S mingw-w64-x86_64-gcc make
```

If it tells you to close the terminal and restart, do that, then run again.

You can verify the compiler installation from this terminal with:
```bash
gcc --version
```

---

### 4. Add MinGW to the Windows PATH

To use gcc and make directly from PowerShell, add their location to your system PATH.

Run this once in PowerShell:
```powershell 
setx PATH "$($env:PATH);C:\msys64\mingw64\bin"
```

Then close and reopen PowerShell, and verify:

```powershell 
gcc --version
```

### 5. Configure and build your project with CMake

#### 5.1 Using CMake Tools extension for VS Code

If you are using VS Code as editor, you install the CMake Tools extension from Microsoft. With that extension it easy and convenient to build a project and execute the tests. 
In the screenshot below, you can see how to set up the correct build folder. Open the CMake Tools extension settings by clicking on the CMake Tools icon in the tool bar on the left, then click on the settings icon (little gear next to "PROJECT STATUS"). The settings will open and you search for "build". The setting CMake Build Directory needs to be: `${workspaceFolder}/src/AKKJ-Build-Breaker/build`. 

Under "PROJECT STATUS -> Configure" the compiler, that we have installed in the previous steps, needs to be selected. 

With everything being set up, one can press the build button in the bottom bar and the project should be built.

![cmake_tools_setup](pictures\screenshot_vscode_cmake_tools_setup.png)


#### 5.2 Using CMake from the PowerShell Terminal
Now you can use CMake from PowerShell to configure and build your project:

```powershell 
cmake -G "MinGW Makefiles" -S . -B build
cmake --build build
```

---

## Running the Tests

Tests are located in the `tests` folder. Assuming the project is built:

### Using VS Code
- Use the **CMake Tools** extension for a GUI to run tests.

### Using the Terminal
1. Navigate to the `build` folder.
2. Run:
    ```bash
    ctest
    ```
3. Enjoy! 🎉


