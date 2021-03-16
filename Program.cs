using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace mandelbrot
{
    class Program
    {
        static void Main(string[] args)
        {
            int height = 2160; //height of the image in px
            int maxIter = 1000; //maximum number of iterations
            int threshold = 100; //number of iterations considered as white

            int width = Convert.ToInt32(1.75 * height);
            double invSize = 1d/(width * height);
            Canvas canvas = new Canvas(width, height);
            int col = 0;
            double x = 0, y = 0;
            double x0, y0, tempX, iter;
            double invMax = 1d/threshold;
            double xScale = 3.5/width, yScale = 2d/height;

            for (int Px = 0; Px < width; Px++) {
                for (int Py = 0; Py < height; Py++) {
                    x0 = (Px * xScale) - 2.5;
                    y0 = (Py * yScale) - 1;
                    x = y = iter = col = 0;
                    while (x*x + y*y <= 0xFFFF && iter < maxIter) {
                        tempX = x*x - y*y + x0;
                        y = 2*x*y + y0;
                        x = tempX;
                        iter++;
                    }
                    if (iter < maxIter) {
                        iter += 1 - Math.Log2(Math.Log2(x*x + y*y) / 2);
                        col = Convert.ToInt32(255*Math.Min(iter*invMax,1));
                    }
                    canvas.SetPixel(Px, Py, Color.FromArgb(col, col, col));
                }
            }

            canvas.Bitmap.Save("yeah.png");
        }
    }


    class Canvas
    {
        public Bitmap Bitmap {get;set;}
        Int32[] Bits {get;set;}
        int Width {get;set;}
        int Height {get;set;}
        protected GCHandle BitsHandle {get;set;}

        public Canvas(int width, int height) {
            this.Width = width;
            this.Height = height;
            this.Bits = new Int32[width * height];
            this.BitsHandle = GCHandle.Alloc(Bits, GCHandleType.Pinned);
            this.Bitmap = new Bitmap(width, height, width * 4,
                PixelFormat.Format32bppPArgb, BitsHandle.AddrOfPinnedObject());
        }

        public void SetPixel(int x, int y, Color colour) {
            Bits[x + (y * Width)] = colour.ToArgb();
        }

        public Color GetPixel(int x, int y) {
            return Color.FromArgb(Bits[x + (y * Width)]);
        }
    }
}