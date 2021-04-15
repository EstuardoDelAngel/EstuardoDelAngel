#include <nds.h>
#include <stdio.h>
#include <gl2d.h>
#include <array>
#include <algorithm>

#define GRAY RGB15(15, 15, 15)
#define WHITE RGB15(31, 31, 31)

#define CELL_SIZE 16
#define WIDTH 256/CELL_SIZE
#define HEIGHT 192/CELL_SIZE
#define SPEED 20

std::array<std::array<bool,HEIGHT>,WIDTH> init_alive = {};
std::array<std::array<bool,HEIGHT>,WIDTH> alive = {};
u_int32_t keys;
touchPosition touch_xy;
int counter = 0;
bool touch = false;


inline void draw_cell(int i, int j)
{
	glBoxFilled(
		CELL_SIZE * i,  CELL_SIZE * j,
		CELL_SIZE * (i + 1) - 1,  CELL_SIZE * (j + 1) - 1,
		WHITE
	);
}

bool next_state(int x, int y)
{
	bool cur = alive[x][y];
	int neighbours = -cur;

	for (int i = std::max(x-1, 0); i <= std::min(x+1, WIDTH); i++) {
		for (int j = std::max(y-1, 0); j <= std::min(y+1, HEIGHT); j++) {
			if (alive[i][j])
				neighbours++;
		}
	}

	if (!cur) {
		if (neighbours == 3)
			return true;
	}
	else if (neighbours == 2 || neighbours == 3)
		return true;
	}

	return false;
}


bool start()
{
	iprintf(
		"\x1b[10;0HPress START to reset"
		"\x1b[16;0HPress A to start life"
		"\x1b[22;0HHOLD L while drawing to delete"
	);

	if (touch_xy.px == 0 && touch_xy.py == 0) {
		touch = false;
	}
	else {
		if (!touch) {
			init_alive[touch_xy.px / CELL_SIZE][touch_xy.py / CELL_SIZE] = !(keysHeld() & KEY_L);
			touch = true;
		}
	}
		

	if (keys & KEY_START) {
		for (auto &i : init_alive) {
			for (auto &j : i)
				j = false;
		}
	}

	for (int i = 0; i < WIDTH; i++) {
		for (int j = 0; j < HEIGHT; j++) {
			if (init_alive[i][j])
				draw_cell(i, j);
		}
	}

	if (keys & KEY_A)
		return true;
	return false;
}


bool play()
{
	iprintf("\x1b[2J");
	iprintf("\x1b[10;0HPress START to reset");

	counter++;
	
	if (counter >= SPEED) {
		counter = 0;
		std::array<std::array<bool,HEIGHT>,WIDTH> next;

		for (int i = 0; i < WIDTH; i++) {
			for (int j = 0; j < HEIGHT; j++) {
				next[i][j] = next_state(i, j);
			}
		}

		alive = next;
	}

	for (int i = 0; i < WIDTH; i++) {
		for (int j = 0; j < HEIGHT; j++) {
			if (alive[i][j])
				draw_cell(i, j);
		}
	}

	if (keys & KEY_START)
		return true;
	return false;
}


int main(int argc, char *argv[])
{
	videoSetMode(MODE_5_3D);
	lcdMainOnBottom();
	consoleDemoInit();
	glScreen2D();
	bool (*update)() = &start;

	while (true)
	{
		scanKeys();
		keys = keysDown();
		touchRead(&touch_xy);
		glBegin2D();
		
		for (int i = 0; i < 256; i += CELL_SIZE) 
			glLine(i, 0, i, 192, GRAY);
	
		for (int i = 0; i < 192; i += CELL_SIZE)
			glLine(0, i, 255, i, GRAY);

		if (update()) {
			if (update == &start) {
				alive = init_alive;
				update = &play;
			}
			else {
				update = &start;
			}
		}

		glEnd2D();
		glFlush(0);
		swiWaitForVBlank();
	}

	return 0;
	
}