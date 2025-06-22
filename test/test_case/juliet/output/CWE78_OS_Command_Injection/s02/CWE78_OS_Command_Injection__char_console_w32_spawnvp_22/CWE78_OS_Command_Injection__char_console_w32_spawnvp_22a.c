# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 1
# 38 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/stdio.h" 1
# 39 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/stdlib.h" 1
# 40 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/stddef.h" 1
# 41 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/time.h" 1
# 42 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/limits.h" 1
# 43 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/string.h" 1
# 44 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/stdint.h" 1
# 45 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2


# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/stdint.h" 1
# 48 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/ctype.h" 1
# 50 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/fcntl.h" 1
# 51 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/types.h" 1
# 52 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/stat.h" 1
# 53 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 96 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h"
typedef struct _twoIntsStruct
{
    int intOne;
    int intTwo;
} twoIntsStruct;
# 109 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h"
extern const int GLOBAL_CONST_TRUE;
extern const int GLOBAL_CONST_FALSE;
extern const int GLOBAL_CONST_FIVE;




extern int globalTrue;
extern int globalFalse;
extern int globalFive;





# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase_io.h" 1







# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 1
# 9 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase_io.h" 2





void printLine(const char * line);

void printWLine(const wchar_t * line);

void printIntLine (int intNumber);

void printShortLine (short shortNumber);

void printFloatLine (float floatNumber);

void printLongLine(long longNumber);

void printLongLongLine(int64_t longLongIntNumber);

void printSizeTLine(size_t sizeTNumber);

void printHexCharLine(char charHex);

void printWcharLine(wchar_t wideChar);

void printUnsignedLine(unsigned unsignedNumber);

void printHexUnsignedCharLine(unsigned char unsignedCharacter);

void printDoubleLine(double doubleNumber);

void printStructLine(const twoIntsStruct * structTwoIntsStruct);

void printBytesLine(const unsigned char * bytes, size_t numBytes);

size_t decodeHexChars(unsigned char * bytes, size_t numBytes, const char * hex);

size_t decodeHexWChars(unsigned char * bytes, size_t numBytes, const wchar_t * hex);

int globalReturnsTrue();

int globalReturnsFalse();

int globalReturnsTrueOrFalse();


extern int globalArgc;
extern char** globalArgv;
# 125 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c" 2







# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/process.h" 1
# 37 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c" 2




int CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_badGlobal = 0;

char * CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_badSource(char * data);

void CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_bad()
{
    char * data;
    char dataBuffer[100] = "ls ";
    data = dataBuffer;
    CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_badGlobal = 1;
    data = CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_badSource(data);
    {
        char *args[] = {"/bin/sh", "-c", data, NULL};



        _spawnvp(_P_WAIT, "sh", args);
    }
}






int CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B1Global = 0;
int CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B2Global = 0;


char * CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B1Source(char * data);

static void goodG2B1()
{
    char * data;
    char dataBuffer[100] = "ls ";
    data = dataBuffer;
    CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B1Global = 0;
    data = CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B1Source(data);
    {
        char *args[] = {"/bin/sh", "-c", data, NULL};



        _spawnvp(_P_WAIT, "sh", args);
    }
}


char * CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B2Source(char * data);

static void goodG2B2()
{
    char * data;
    char dataBuffer[100] = "ls ";
    data = dataBuffer;
    CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B2Global = 1;
    data = CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_goodG2B2Source(data);
    {
        char *args[] = {"/bin/sh", "-c", data, NULL};



        _spawnvp(_P_WAIT, "sh", args);
    }
}

void CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_good()
{
    goodG2B1();
    goodG2B2();
}
# 123 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s02/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22/CWE78_OS_Command_Injection__char_console_w32_spawnvp_22a.c"
int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    CWE78_OS_Command_Injection__char_console_w32_spawnvp_22_bad();
    printLine("Finished bad()");

    return 0;
}
