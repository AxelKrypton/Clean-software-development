#include "su2.hpp"
#include <iostream>

int main() {
  // take power of a su2 matrix
  SU2_mat a(1.0, 0.0, 0.0, 0.0);
  a = a * a; // should be -1,0,0,0

  // formatted output of su2 matrix
  std::cout << a.c0 << " " << a.c1 << " " << a.c2 << " " << a.c3 << "\n";

  return 0;
}