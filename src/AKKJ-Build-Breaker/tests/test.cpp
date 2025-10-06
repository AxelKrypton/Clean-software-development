#include <vir/test.h>

TEST(test_name) {
  VERIFY(1 > 0);
  COMPARE(1, 1);

  struct A {
    int x;
  };
  COMPARE(A(), A());    // implicitly does memcmp
  MEMCOMPARE(A(), A()); // explicitly does memcmp
}