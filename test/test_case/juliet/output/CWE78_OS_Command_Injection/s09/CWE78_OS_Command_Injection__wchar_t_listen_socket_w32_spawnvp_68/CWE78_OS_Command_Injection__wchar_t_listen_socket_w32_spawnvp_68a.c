# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
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
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 43 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/types.h" 1
# 44 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/socket.h" 1
# 45 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/netinet/in.h" 1
# 46 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/arpa/inet.h" 1
# 47 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2
# 56 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/process.h" 1
# 57 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c" 2

wchar_t * CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_badData;
wchar_t * CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_goodG2BData;




void CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68b_badSink();

void CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_bad()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;
    {




        int recvResult;
        struct sockaddr_in service;
        wchar_t *replace;
        int listenSocket = -1;
        int acceptSocket = -1;
        size_t dataLen = wcslen(data);
        do
        {
# 92 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
            listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            if (listenSocket == -1)
            {
                break;
            }
            memset(&service, 0, sizeof(service));
            service.sin_family = AF_INET;
            service.sin_addr.s_addr = INADDR_ANY;
            service.sin_port = htons(27015);
            if (bind(listenSocket, (struct sockaddr*)&service, sizeof(service)) == -1)
            {
                break;
            }
            if (listen(listenSocket, 5) == -1)
            {
                break;
            }
            acceptSocket = accept(listenSocket, NULL, NULL);
            if (acceptSocket == -1)
            {
                break;
            }

            recvResult = recv(acceptSocket, (char *)(data + dataLen), sizeof(wchar_t) * (100 - dataLen - 1), 0);
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
        if (listenSocket != -1)
        {
            close(listenSocket);
        }
        if (acceptSocket != -1)
        {
            close(acceptSocket);
        }






    }
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_badData = data;
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68b_badSink();
}






void CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68b_goodG2BSink();


static void goodG2B()
{
    wchar_t * data;
    wchar_t dataBuffer[100] = L"ls ";
    data = dataBuffer;

    wcscat(data, L"*.*");
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_goodG2BData = data;
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68b_goodG2BSink();
}

void CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_good()
{
    goodG2B();
}
# 188 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s09/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68/CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68a.c"
int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    CWE78_OS_Command_Injection__wchar_t_listen_socket_w32_spawnvp_68_bad();
    printLine("Finished bad()");

    return 0;
}
