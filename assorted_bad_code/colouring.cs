using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Collections.Generic;

//Generates pattern using depth first search and random colouring

namespace graphx
{
    class Program
    {
        static void Main(string[] args)
        {
            int width = 1000;
            int height = 1000;
            //double probability = 0.0005f;

            Canvas canvas = new Canvas(width, height);
            int counter = 0;
            Random rand = new Random();
            int[] cur;
            int[] chosen;
            Color curColor = Color.FromArgb(255, Color.FromArgb(rand.Next()));
            Color blank = Color.FromArgb(0,0,0,0);
            Stack<int[]> path = new Stack<int[]>();
            List<int[]> neighbours;
            path.Push(new[] {0,0});
            canvas.SetPixel(0, 0, curColor);

            while (path.Count > 0) {
                cur = path.Pop();
                curColor = canvas.GetPixel(cur[0], cur[1]);
                neighbours = new List<int[]>();
                int minX = cur[0]-1, maxX = cur[0]+1;
                int minY = cur[1]-1, maxY = cur[1]+1;

                if (minX >= 0 && canvas.GetPixel(minX, cur[1]) == blank) {
                    neighbours.Add(new[] {minX, cur[1]}); }
                if (maxX < width && canvas.GetPixel(maxX, cur[1]) == blank) {
                    neighbours.Add(new[] {maxX, cur[1]}); }
                if (minY >= 0 && canvas.GetPixel(cur[0], minY) == blank) {
                    neighbours.Add(new[] {cur[0], minY}); }
                if (maxY < height && canvas.GetPixel(cur[0], maxY) == blank) {
                    neighbours.Add(new[] {cur[0], maxY}); }

                if (neighbours.Count > 0) {
                    path.Push(cur);
                    chosen = neighbours[rand.Next(neighbours.Count)];
                    counter++;
                    if (counter > 10000) {
                        counter = 0;
                        curColor = Color.FromArgb(255, Color.FromArgb(rand.Next()));
                    }
                    canvas.SetPixel(chosen[0], chosen[1], curColor);
                    path.Push(chosen);
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
