#pragma once

#include <cmath>

class SU2_mat {
public:
  double c0, c1, c2, c3;
  SU2_mat(double c0, double c1, double c2, double c3);
  SU2_mat();
  SU2_mat(SU2_mat const &obj);

  SU2_mat operator+(SU2_mat const &obj);
  void operator+=(SU2_mat const &obj);
  SU2_mat operator-(SU2_mat const &obj);
  void operator-=(SU2_mat const &obj);
  SU2_mat operator*(SU2_mat const &obj);
  void operator*=(SU2_mat const &obj);
  void operator*=(double const &i);
  void operator/=(double const &i);

  void operator=(SU2_mat const &obj);

  SU2_mat dag();

  SU2_mat unit();

  SU2_mat pow(int);

  double trace();

  double det();

  void mk_dble_array_sun(double u[4]);

  void project_to_sun();
};

SU2_mat operator*(SU2_mat const &obj, double const &i);
SU2_mat operator*(double const &i, SU2_mat const &obj);

SU2_mat operator/(SU2_mat const &obj, double const &i);