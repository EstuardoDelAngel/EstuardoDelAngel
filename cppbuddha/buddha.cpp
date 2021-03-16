#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>

using namespace std;

struct point
{
    double x, y;
};

int main()
{
    const int W = 2160;
    const int bailout = 50;
    const long maxN = 1 << 23;

    const double sqrt8 = sqrt(8);

    double x, y, x0, y0, tempX;
    int iter, ix, iy;
    point seq[bailout];
    u_char image[W*W] = {};
    
    for (long n = 0; n < maxN; n++)
    {
        x = x0 = 4 * drand48() - 2;
        y = y0 = 4 * drand48() - 2;
        iter = 0;

        while (x*x + y*y < sqrt8 && iter < bailout)
        {
            tempX = x*x - y*y + x0;
            y = 2*x*y + y0;
            x = tempX;
            seq[iter].x = x;
            seq[iter].y = y;
            iter++;
        }

        if (iter < bailout)
        {
            for (int i = 0; i < iter; i++)
            {
                ix = int(0.25 * W * (seq[i].x + 2));
                iy = int(0.25 * W * (seq[i].y + 2));
                if (ix >= 0 && iy >= 0 && ix < W && iy < W) image[W*iy + ix]++;
            }
        }
        if (n%10000==0) cout << n << "\n";
    }

    double invMax = 1.0/double(*max_element(begin(image), end(image)));
    int col;

    FILE * file = fopen("buddha.ppm", "w");
    fprintf(file, "P3\n%i %i\n255\n", W, W);

    for (int i = 0; i < W*W; i++)
    {
        col = int(255 * sqrt(image[i]*invMax));
        fprintf(file, "%i %i %i ", col, col, col);
    }

    fclose(file);
    return 0;
}