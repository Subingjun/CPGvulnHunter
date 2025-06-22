# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
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
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c" 2
# 53 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
void CWE78_OS_Command_Injection__wchar_t_environment_execl_32_bad()
{
    wchar_t * data;
    wchar_t * *dataPtr1 = &data;
    wchar_t * *dataPtr2 = &data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    {
        wchar_t * data = *dataPtr1;
        {

            size_t dataLen = wcslen(data);
            wchar_t * environment = getenv(L"ADD");

            if (environment != NULL)
            {

                wcsncat(data+dataLen, environment, 100-dataLen-1);
            }
        }
        *dataPtr1 = data;
    }
    {
        wchar_t * data = *dataPtr2;


        execl(L"/bin/sh", L"/bin/sh", L"-c", data, NULL);
    }
}






static void goodG2B()
{
    wchar_t * data;
    wchar_t * *dataPtr1 = &data;
    wchar_t * *dataPtr2 = &data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    {
        wchar_t * data = *dataPtr1;

        wcscat(data, L"*.*");
        *dataPtr1 = data;
    }
    {
        wchar_t * data = *dataPtr2;


        execl(L"/bin/sh", L"/bin/sh", L"-c", data, NULL);
    }
}

void CWE78_OS_Command_Injection__wchar_t_environment_execl_32_good()
{
    goodG2B();
}
# 123 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s06/CWE78_OS_Command_Injection__wchar_t_environment_execl_32/CWE78_OS_Command_Injection__wchar_t_environment_execl_32.c"
int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    CWE78_OS_Command_Injection__wchar_t_environment_execl_32_good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    CWE78_OS_Command_Injection__wchar_t_environment_execl_32_bad();
    printLine("Finished bad()");

    return 0;
}
