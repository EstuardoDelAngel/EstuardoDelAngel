using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Collections.Generic;

namespace graphx2
{
    class Program
    {
        static void Main(string[] args)
        {
            int width = 1000;
            int height = 1000;
            int number = 100;
            int threshold = 170; 

            Canvas canvas = new Canvas(width, height);
            Random rand = new Random();
            Color blank = Color.FromArgb(0);
            List<int[]> points = new List<int[]>();
            Color col;
            int x, y, b;
            int[] xs, ys;
            double theta, x0, y0;
            double froot2 = 4 * Math.Sqrt(2);
            double pi2 = 2 * Math.PI;
            double invThresh = 1d/threshold;
            int r = 2;
            bool full = false;

            for (int i = 0; i < number; i++) {
                col = Color.Black;
                x = rand.Next(width); y = rand.Next(height);
                points.Add(new[] {x, y});
                canvas.SetPixel(x, y, col);
            }

            while (!full) {
                theta = 1/(froot2 * r);
                full = true;
                b = Math.Max(255 - Convert.ToInt32(255 * r * invThresh), 0);
                col = Color.FromArgb(b, b, b);

                foreach (int[] point in points) {
                    for (double t = 0; t < pi2; t += theta) {
                        x0 = r * Math.Sin(t) + point[0];
                        y0 = r * Math.Cos(t) + point[1];
                        xs = new[] {Convert.ToInt32(Math.Floor(x0)), 
                        Convert.ToInt32(Math.Ceiling(x0))};
                        ys = new[] {Convert.ToInt32(Math.Floor(y0)), 
                        Convert.ToInt32(Math.Ceiling(y0))};

                        foreach (int xn in xs) {
                            if (xn >= 0 && xn < width) {
                                foreach (int yn in ys) {
                                    if (yn >= 0 && yn < height && canvas.GetPixel(xn, yn) == blank) {
                                        full = false;
                                        canvas.SetPixel(xn, yn, col);
                                    }
                                }
                            }
                        }
                    }
                }

                r++;
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
