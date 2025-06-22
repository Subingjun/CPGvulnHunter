# 0 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
# 17 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
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
# 18 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2

# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/wchar.h" 1
# 20 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 28 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/unistd.h" 1
# 29 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 43 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/types.h" 1
# 44 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/sys/socket.h" 1
# 45 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/netinet/in.h" 1
# 46 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/arpa/inet.h" 1
# 47 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2
# 56 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
# 1 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/minimal_headers/process.h" 1
# 57 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c" 2

typedef struct _CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType
{
    char * structFirst;
} CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType;




void CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67b_badSink(CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType myStruct);

void CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_bad()
{
    char * data;
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType myStruct;
    char dataBuffer[100] = "ls ";
    data = dataBuffer;
    {




        int recvResult;
        struct sockaddr_in service;
        char *replace;
        int listenSocket = -1;
        int acceptSocket = -1;
        size_t dataLen = strlen(data);
        do
        {
# 95 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
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

            recvResult = recv(acceptSocket, (char *)(data + dataLen), sizeof(char) * (100 - dataLen - 1), 0);
            if (recvResult == -1 || recvResult == 0)
            {
                break;
            }

            data[dataLen + recvResult / sizeof(char)] = '\0';

            replace = strchr(data, '\r');
            if (replace)
            {
                *replace = '\0';
            }
            replace = strchr(data, '\n');
            if (replace)
            {
                *replace = '\0';
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
    myStruct.structFirst = data;
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67b_badSink(myStruct);
}






void CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67b_goodG2BSink(CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType myStruct);

static void goodG2B()
{
    char * data;
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_structType myStruct;
    char dataBuffer[100] = "ls ";
    data = dataBuffer;

    strcat(data, "*.*");
    myStruct.structFirst = data;
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67b_goodG2BSink(myStruct);
}

void CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_good()
{
    goodG2B();
}
# 191 "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/organized_cwe/CWE78_OS_Command_Injection/s04/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67/CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67a.c"
int main(int argc, char * argv[])
{

    srand( (unsigned)time(NULL) );

    printLine("Calling good()...");
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_good();
    printLine("Finished good()");


    printLine("Calling bad()...");
    CWE78_OS_Command_Injection__char_listen_socket_w32_spawnlp_67_bad();
    printLine("Finished bad()");

    return 0;
}
