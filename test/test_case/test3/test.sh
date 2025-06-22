        gcc -E -nostdinc  \
        -I"$INCLUDE_DIR" \
        -DINCLUDEMAIN \
          /home/nstl/data/CPGvulnHunter/test/test_case/test3/CWE78_OS_Command_Injection__char_connect_socket_execl_01.c  > ./output.c