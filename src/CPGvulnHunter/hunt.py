if __name__ == "__main__":
    from CPGvulnHunter.core.engine import VulnerabilityEngine
    config_file = "/home/nstl/data/CPGvulnHunter/config.yml"
    taget_src_path = "/home/nstl/data/CPGvulnHunter/test/test_case/juliet/output/CWE78_OS_Command_Injection/s01/CWE78_OS_Command_Injection__char_connect_socket_execl_01"
    VulnerabilityEngine(config_file=config_file).run(src_path=taget_src_path, passes=["cwe78"])
    