#include "su2.hpp"

#include <array>
#include <cmath>
#include <stdexcept>

SU2_mat::SU2_mat(SU2_mat const &obj) {
  c0 = obj.c0;
  c1 = obj.c1;
  c2 = obj.c2;
  c3 = obj.c3;
}

SU2_mat::SU2_mat(double _c0, double _c1, double _c2, double _c3) {
  c0 = _c0;
  c1 = _c1;
  c2 = _c2;
  c3 = _c3;
}

SU2_mat SU2_mat::operator+(SU2_mat const &obj) {
  return SU2_mat(c0 + obj.c0, c1 + obj.c1, c2 + obj.c2, c3 + obj.c3);
}

void SU2_mat::operator+=(SU2_mat const &obj) { *this = *this + obj; }

SU2_mat SU2_mat::operator-(SU2_mat const &obj) {
  return SU2_mat(c0 - obj.c0, c1 - obj.c1, c2 - obj.c2, c3 - obj.c3);
}

void SU2_mat::operator-=(SU2_mat const &obj) { *this = *this - obj; }

SU2_mat SU2_mat::operator*(SU2_mat const &obj) {
  double res_c0, res_c1, res_c2, res_c3;
  res_c0 = c0 * obj.c0 - c1 * obj.c1 - c2 * obj.c2 - c3 * obj.c3;
  res_c1 = c0 * obj.c1 + c1 * obj.c0 - c2 * obj.c3 + c3 * obj.c2;
  res_c2 = c0 * obj.c2 + c1 * obj.c3 + c2 * obj.c0 - c3 * obj.c1;
  res_c3 = c0 * obj.c3 - c1 * obj.c2 + c2 * obj.c1 + c3 * obj.c0;
  return SU2_mat(res_c0, res_c1, res_c2, res_c3);
}

void SU2_mat::operator*=(SU2_mat const &obj) { *this = *this * obj; }

void SU2_mat::operator*=(double const &value) { return *this = *this * value; }

void SU2_mat::operator/=(double const &value) {
  if (0.0 == value) throw std::invalid_argument("division by 0.0");
  return *this = *this / value;
}

void SU2_mat::operator=(SU2_mat const &obj) {
  c0 = obj.c0;
  c1 = obj.c1;
  c2 = obj.c2;
  c3 = obj.c3;
}

// TODO: Currently only total tolerance considered.
//       Better: combination of relative and total tolerance.
bool SU2_mat::operator==(SU2_mat const &obj) const {
  return (std::fabs(c0 - obj.c0) < epsilon) &&
         (std::fabs(c1 - obj.c1) < epsilon) &&
         (std::fabs(c2 - obj.c2) < epsilon) &&
         (std::fabs(c3 - obj.c3) < epsilon);
}

SU2_mat SU2_mat::dag() { return SU2_mat(c0, -c1, -c2, -c3); }

SU2_mat SU2_mat::unit() { return SU2_mat(1.0, 0.0, 0.0, 0.0); }

double SU2_mat::trace() { return 2 * c0; }

double SU2_mat::det() { return std::fabs(c0 * c0 + c1 * c1 + c2 * c2 + c3 * c3); }

void SU2_mat::mk_dble_array_sun(const std::array<double, 4>& u) {
  c0 = u[0];
  c1 = u[1];
  c2 = u[2];
  c3 = u[3];
}

void SU2_mat::project_to_sun() { *this /= std::sqrt((*this).det()); }

SU2_mat operator*(SU2_mat const &obj, double const &value) {
  return SU2_mat(obj.c0 * value, obj.c1 * value, obj.c2 * value, obj.c3 * value);
}

SU2_mat operator*(double const &value, SU2_mat const &obj) { return obj * value; }

SU2_mat operator/(SU2_mat const &obj, double const &value) {
  if (0.0 == value) throw std::invalid_argument("division by 0.0");
  return SU2_mat(obj.c0 / value, obj.c1 / value, obj.c2 / value, obj.c3 / value);
}

SU2_mat SU2_mat::pow(int n) {
  SU2_mat result = SU2_mat::unit();
  for (int i = 0; i < n; ++i) {
    result *= *this;
  }
  return result;
}