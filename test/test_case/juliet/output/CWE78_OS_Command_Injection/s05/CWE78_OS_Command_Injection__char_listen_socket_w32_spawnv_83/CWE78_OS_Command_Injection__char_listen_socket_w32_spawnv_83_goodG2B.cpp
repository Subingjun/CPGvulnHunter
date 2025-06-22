# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp"
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp"
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





# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/new" 1
# 59 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2


class TwoIntsClass
{
    public:
        int intOne;
        int intTwo;
};

class OneIntClass
{
    public:
        int intOne;
};
# 96 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h"
typedef struct _twoIntsStruct
{
    int intOne;
    int intTwo;
} twoIntsStruct;


extern "C" {





extern const int GLOBAL_CONST_TRUE;
extern const int GLOBAL_CONST_FALSE;
extern const int GLOBAL_CONST_FIVE;




extern int globalTrue;
extern int globalFalse;
extern int globalFive;


}


# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase_io.h" 1







# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 1
# 9 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase_io.h" 2


extern "C" {


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


}
# 125 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/C/testcasesupport/std_testcase.h" 2
# 19 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83.h" 1
# 19 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83.h"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83.h" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83.h"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83.h" 2







namespace CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83
{



class CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_bad
{
public:
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_bad(char * dataCopy);
    ~CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_bad();

private:
    char * data;
};





class CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B
{
public:
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B(char * dataCopy);
    ~CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B();

private:
    char * data;
};



}
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/process.h" 1
# 22 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B.cpp" 2

namespace CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83
{
CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B::CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B(char * dataCopy)
{
    data = dataCopy;

    strcat(data, "*.*");
}

CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B::~CWE78_OS_Command_Injection__char_listen_socket_w32_spawnv_83_goodG2B()
{
    {
        char *args[] = {"/bin/sh", "-c", data, NULL};


        _spawnv(_P_WAIT, "/bin/sh", args);
    }
}
}
