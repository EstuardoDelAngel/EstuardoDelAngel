//add comment support
//formatting flags
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <cstdlib>
#include <thread>
#include <chrono>

using namespace std;

inline void error(string msg)
{
    cout << msg << endl;
    exit(-1);
}


inline void tokenize(string str, string *arr, int n)
{
    stringstream ssin;
    ssin << str;

    int i = 0;
    while (i < n && ssin.good()) {
        ssin >> arr[i];
        i++;
    }

    if (ssin.good()) error("Syntax error");
    return;
}


int main(int argc, char *argv[]) 
{
    char *p;
    int delay;

    switch (argc) {
        case 2:
            delay = 0;
            break;

        case 3:
            delay = strtol(argv[2], &p, 10);
            if (*p != 0) error("Invalid number");
            break;

        default:
            error("Error--arguments must be:\n"
            "Required: file name\n"
            "Optional: delay (ms, default = 0)");
            break;
    }

    map<string, int> opcodes; {
        opcodes["HLT"] = 0;
        opcodes["DAT"] = 0;
        opcodes["ADD"] = 100;
        opcodes["SUB"] = 200;
        opcodes["STA"] = 300;
        opcodes["LDA"] = 500;
        opcodes["BRA"] = 600;
        opcodes["BRZ"] = 700;
        opcodes["BRP"] = 800;
        opcodes["INP"] = 901;
        opcodes["OUT"] = 902;
    }
    
    ifstream file(argv[1]);
    if (file.fail()) error("Error--file does not exist");

    string line;
    map<string, int> pointers;
    map<string, int>::iterator it;
    string text[100][3]  = {};
    string operands[100] = {};
    int RAM[100] = {};


    int i = 0;
    while (getline(file, line)) {
        tokenize(line, text[i], 3);

        int lineLen = 0;
        for (int k = 0; k < 3; k++) lineLen += text[i][k].length();
        if (lineLen == 0) continue;

        int j = 1;
        it = opcodes.find(text[i][0]);

        if (it == opcodes.end()) {
            pointers[text[i][0]] = i;
            j = 2;
            it = opcodes.find(text[i][1]);
        } 
        
        if (it == opcodes.end()) error("Syntax error");
        else RAM[i] = it->second;

        operands[i] = text[i][j];
        i++;
    }


    for (i = 0; i < 100; i++) {
        int operand;
        it = pointers.find(operands[i]);

        if (it != pointers.end()) {
            operand = it->second;
        } else {
            operand = strtol(operands[i].c_str(), &p, 10);
            if (*p != 0 || operand > 99) error("Syntax error");
        }

        RAM[i] += operand;
    }


    int ACC = 0; 
    int PC  = 0;
    div_t CIR;
    bool done = false;

    do {
        CIR = div(RAM[PC], 100);

        switch (CIR.quot) {
            case 1: ACC += RAM[CIR.rem]; break;
            case 2: ACC -= RAM[CIR.rem]; break;
            case 3: RAM[CIR.rem] = ACC;  break;
            case 5: ACC = RAM[CIR.rem];  break;

            case 6:
                PC = CIR.rem;
                continue;
                break;

            case 7:
                if (ACC == 0) {
                    PC = CIR.rem;
                    continue;
                }
                break;

            case 8:
                if (ACC >= 0) {
                    PC = CIR.rem;
                    continue;
                }
                break;

            case 9:
                if (CIR.rem == 1) {
                    cout << "User input: ";
                    cin >> ACC;
                } else if (CIR.rem == 2) {
                    cout << ACC << endl;
                } else {
                    done = true;
                }
                break;

            default:
                done = true;
                break;
        }

        PC++;
        this_thread::sleep_for(chrono::milliseconds(delay));
    } while (!done && PC < 100);

    return 0;
}