/**
 * This code was adapted from: https://www.gem5.org/documentation/learning_gem5/gem5_101/homework-3
 */

#include <charconv>
#include <iostream>
#include <random>

#include <gem5/m5ops.h>

void generate_data(double y[], double x[], int n)
{
  std::random_device rd; std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(1, 2);

  for (int i = 0; i < n; ++i)
  {
    x[i] = dis(gen);
    y[i] = dis(gen);
  }
}

double reduce(double y[], int n)
{
  double sum = 0.0;

  for (int i = 0; i < n; ++i)
  {
    sum += y[i];
  }

  return sum;
}

void daxpy(double y[], double a, double x[], int n) {
    for (int i = 0; i < n; i++) {
        y[i] = a*x[i] + y[i];
    }
}

int main(int argc, char **argv)
{
  int N;
  if(argc == 2) {
    std::string strN(argv[1]);
    std::from_chars(strN.data(), strN.data() + strN.size(), N);
  } else {
    N = 1000;
  }

  double X[N], Y[N], alpha = 0.5;
  generate_data(X, Y, N);

  m5_dump_reset_stats(0, 0);
  daxpy(Y, alpha, X, N);
  m5_dump_reset_stats(0, 0);

  std::cout << reduce(Y, N) << std::endl;

  return 0;
}

