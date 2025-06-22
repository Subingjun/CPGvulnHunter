# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
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
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c" 2
# 44 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/process.h" 1
# 45 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c" 2




static int badStatic = 0;

static wchar_t * badSource(wchar_t * data)
{
    if(badStatic)
    {
        {

            size_t dataLen = wcslen(data);
            wchar_t * environment = getenv(L"ADD");

            if (environment != NULL)
            {

                wcsncat(data+dataLen, environment, 100-dataLen-1);
            }
        }
    }
    return data;
}

void CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21_bad()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    badStatic = 1;
    data = badSource(data);
    {
        wchar_t *args[] = {L"/bin/sh", L"-c", data, NULL};


        _wspawnv(_P_WAIT, L"/bin/sh", args);
    }
}






static int goodG2B1Static = 0;
static int goodG2B2Static = 0;


static wchar_t * goodG2B1Source(wchar_t * data)
{
    if(goodG2B1Static)
    {

        printLine("Benign, fixed string");
    }
    else
    {

        wcscat(data, L"*.*");
    }
    return data;
}

static void goodG2B1()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    goodG2B1Static = 0;
    data = goodG2B1Source(data);
    {
        wchar_t *args[] = {L"/bin/sh", L"-c", data, NULL};


        _wspawnv(_P_WAIT, L"/bin/sh", args);
    }
}


static wchar_t * goodG2B2Source(wchar_t * data)
{
    if(goodG2B2Static)
    {

        wcscat(data, L"*.*");
    }
    return data;
}

static void goodG2B2()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    goodG2B2Static = 1;
    data = goodG2B2Source(data);
    {
        wchar_t *args[] = {L"/bin/sh", L"-c", data, NULL};


        _wspawnv(_P_WAIT, L"/bin/sh", args);
    }
}

void CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21_good()
{
    goodG2B1();
    goodG2B2();
}
# 166 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s07/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21/CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21.c"
int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21_good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    CWE78_OS_Command_Injection__wchar_t_environment_w32_spawnv_21_bad();
    printLine("Finished bad()");

    return 0;
}
