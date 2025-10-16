import os
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith('.')]

    print("请选择一个测试目录：")
    for idx, d in enumerate(test_dirs):
        print(f"{idx+1}. {d}")
    print(f"{idx+1+1}. clean (清理所有生成的 scenario 文件和结果文件)")

    choice = input("输入序号：").strip()
    if choice == str(idx+1+1):
        print("清理所有生成的 scenario 文件和结果文件...")
        for test_dir in test_dirs:
            test_path = os.path.join(base_dir, test_dir)
            for f in os.listdir(test_path):
                if f.startswith("workload") and (f.endswith(".xml") or f.endswith(".txt")) and "_scenario_" in f:
                    os.remove(os.path.join(test_path, f))
                if f.endswith(".log") or f.endswith(".out") or f.endswith(".png"):
                    os.remove(os.path.join(test_path, f))
        print("清理完成。")
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(test_dirs):
        print("输入无效，退出。")
        return

    selected_dir = test_dirs[int(choice)-1]
    test_path = os.path.join(base_dir, selected_dir)

    # 获取所有 ssdconfig 和 workload 文件
    ssdconfigs = [f for f in os.listdir(test_path) if f.startswith("ssdconfig") and f.endswith(".xml")]
    workloads = [f for f in os.listdir(test_path)
                 if f.startswith("workload") and f.endswith(".xml") and "_scenario_" not in f]
    print(ssdconfigs)
    print(workloads)


    if not ssdconfigs or not workloads:
        print("未找到所需的 ssdconfig 或 workload 文件。")
        return

    mqsim_exec = os.path.abspath(os.path.join(base_dir, "..", "MQSim"))
    if not os.path.exists(mqsim_exec):
        print(f"MQSim 可执行文件未找到：{mqsim_exec}")
        return

    print(f"将在目录 {test_path} 下批量运行 MQSim：")
    for ssdconfig in ssdconfigs:
        for workload in workloads:
            cmd = [mqsim_exec, "-i", ssdconfig, "-w", workload]
            print(f"运行：{' '.join(cmd)}")
            subprocess.run(cmd, cwd=test_path)

if __name__ == "__main__":
    main()