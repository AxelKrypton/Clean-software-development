# SU(2) Matrix Operations

The file `su2.cpp` implements the class `SU2_mat` for handling SU(2) matrices.

## Matrix Representation

An SU(2) matrix `U` is represented by four real numbers `(c0, c1, c2, c3)` which form a 2x2 complex matrix as follows:

```
[  c0 + i*c1     c2 + i*c3 ]
U = [ -c2 + i*c3    c0 - i*c1 ]
```

For `U` to be a special unitary matrix, its determinant must be 1. The determinant is given by:
`det(U) = c0^2 + c1^2 + c2^2 + c3^2`
So, the condition `c0^2 + c1^2 + c2^2 + c3^2 = 1` must hold.

## Implemented Operations in `su2.cpp`

The `SU2_mat` class provides several operations on the `(c0, c1, c2, c3)` components:

*   **Constructors**: Default, copy, and from the four components `(c0, c1, c2, c3)`.
*   **Addition/Subtraction (`+`, `-`)**: These are performed component-wise on `(c0, c1, c2, c3)`.
*   **Multiplication (`*`)**: The multiplication of two `SU2_mat` objects, `a` and `b`, is defined by the following formulas for the resulting components `res_c`:
    ```cpp
    res_c0 = a.c0*b.c0 - a.c1*b.c1 - a.c2*b.c2 - a.c3*b.c3;
    res_c1 = a.c0*b.c1 + a.c1*b.c0 - a.c2*b.c3 + a.c3*b.c2;
    res_c2 = a.c0*b.c2 + a.c1*b.c3 + a.c2*b.c0 - a.c3*b.c1;
    res_c3 = a.c0*b.c3 - a.c1*b.c2 + a.c2*b.c1 + a.c3*b.c0;
    ```
    **Note**: This implemented multiplication does not correspond to standard matrix multiplication for the matrix representation given above.
*   **Hermitian Conjugate (`dag()`)**: Returns the hermitian conjugate (dagger) of the matrix. This operation transforms the components `(c0, c1, c2, c3)` to `(c0, -c1, -c2, -c3)`. This is consistent with taking the hermitian conjugate of the matrix representation.
*   **Trace (`trace()`)**: Returns `2*c0`, which is the trace of the matrix.
*   **Determinant (`det()`)**: Returns `c0^2 + c1^2 + c2^2 + c3^2`, the determinant of the matrix.
*   **Projection (`project_to_sun()`)**: Normalizes the matrix to have determinant 1 by dividing all components by `sqrt(det)`. This projects the matrix onto the SU(2) group.
*   

# Running this project on a Windows 11 machine

## Setting up CMake and GCC on Windows 11

These steps describe how to set up a working **CMake + GCC (MinGW)** build environment on **Windows 11** using **PowerShell** and **MSYS2**.  
This allows you to build C/C++ projects similarly to how you would on Linux systems.

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
# If prompted, close and reopen the terminal, then run again:
pacman -Syu
pacman -S mingw-w64-x86_64-gcc make
```

If it tells you to close the terminal and restart, do that, then run again.

You can verify the compiler installation from this terminal with:
```bash
gcc --version
```

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

Now you can use CMake from PowerShell to configure and build your project:

```powershell 
cmake -G "MinGW Makefiles" -S . -B build
cmake --build build
```
If everything is configured correctly, CMake will automatically use GCC from your MSYS2 installation.
