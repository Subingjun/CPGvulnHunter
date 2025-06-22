# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
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
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82.h" 1
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82.h"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 19 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82.h" 2
# 27 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82.h"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82.h" 2







namespace CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82
{

class CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_base
{
public:

    virtual void action(wchar_t * data) = 0;
};



class CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_bad : public CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_base
{
public:
    void action(wchar_t * data);
};





class CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_goodG2B : public CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_base
{
public:
    void action(wchar_t * data);
};



}
# 19 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 27 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/types.h" 1
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/socket.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/netinet/in.h" 1
# 30 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/arpa/inet.h" 1
# 31 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 32 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp" 2
# 41 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
namespace CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82
{



void bad()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    {




        int recvResult;
        struct sockaddr_in service;
        wchar_t *replace;
        int connectSocket = -1;
        size_t dataLen = wcslen(data);
        do
        {
# 71 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
            connectSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            if (connectSocket == -1)
            {
                break;
            }
            memset(&service, 0, sizeof(service));
            service.sin_family = AF_INET;
            service.sin_addr.s_addr = inet_addr("127.0.0.1");
            service.sin_port = htons(27015);
            if (connect(connectSocket, (struct sockaddr*)&service, sizeof(service)) == -1)
            {
                break;
            }



            recvResult = recv(connectSocket, (char *)(data + dataLen), sizeof(wchar_t) * (100 - dataLen - 1), 0);
            if (recvResult == -1 || recvResult == 0)
            {
                break;
            }

            data[dataLen + recvResult / sizeof(wchar_t)] = L'\0';

            replace = wcschr(data, L'\r');
            if (replace)
            {
                *replace = L'\0';
            }
            replace = wcschr(data, L'\n');
            if (replace)
            {
                *replace = L'\0';
            }
        }
        while (0);
        if (connectSocket != -1)
        {
            close(connectSocket);
        }






    }
    CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_base* baseObject = new CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_bad;
    baseObject->action(data);
    delete baseObject;
}






static void goodG2B()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;

    wcscat(data, L"*.*");
    CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_base* baseObject = new CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82_goodG2B;
    baseObject->action(data);
    delete baseObject;
}

void good()
{
    goodG2B();
}



}
# 157 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s05/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82/CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82a.cpp"
using namespace CWE78_OS_Command_Injection__wchar_t_connect_socket_w32spawnl_82;

int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    bad();
    printLine("Finished bad()");

    return 0;
}
