
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

RESULT_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS = ["IOPS", "Bandwidth", "Device_Response_Time", "End_to_End_Request_Delay"]

# 自动列出所有 workload-backend-contention-flow-1-flow-2.xml 文件
workload_files = [f for f in os.listdir(RESULT_DIR)
                  if f.startswith("workload") and f.endswith(".xml") and "_scenario_" not in f]
if not workload_files:
    print("未找到 workload 文件！")
    exit(1)

for workload in workload_files:
    print(f"分析 {workload} 的所有 scenario 结果...")
    # 查找所有对应的 scenario 文件
    prefix = workload.replace('.xml', '_scenario_')
    scenario_files = [f for f in os.listdir(RESULT_DIR)
                      if f.startswith(prefix) and f.endswith('.xml')]
    scenario_files = sorted(scenario_files, key=lambda x: int(x.split('_scenario_')[-1].split('.xml')[0]))
    if not scenario_files:
        print(f"未找到 {workload} 的 scenario 结果文件！")
        continue

    # 统计所有 scenario 的所有流
    flow_names = set()
    scenario_metrics = dict()  # {flow_name: {metric: [values...]}}
    scenario_ids = []
    for scen_file in scenario_files:
        scen_path = os.path.join(RESULT_DIR, scen_file)
        scenario_id = scen_file.split('_scenario_')[-1].split('.xml')[0]
        scenario_ids.append(scenario_id)
        tree = ET.parse(scen_path)
        root = tree.getroot()
        flows = root.findall(".//Host.IO_Flow")
        for flow in flows:
            flow_name = flow.find("Name").text if flow.find("Name") is not None else "flow_unknown"
            flow_names.add(flow_name)
            if flow_name not in scenario_metrics:
                scenario_metrics[flow_name] = {metric: [] for metric in METRICS}
            for metric in METRICS:
                val = flow.find(metric)
                scenario_metrics[flow_name][metric].append(float(val.text) if val is not None else None)

    # 将所有流的同一指标画在同一张图中
    for metric in METRICS:
        plt.figure(figsize=(10,6))
        for flow_name in flow_names:
            plt.plot(scenario_ids, scenario_metrics[flow_name][metric], marker='o', label=flow_name)
        plt.xlabel('Scenario')
        plt.ylabel(metric)
        plt.title(f'{workload} {metric} Comparison (All Flows)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        img_name = f'{workload}_scenario_{metric}_all_flows.png'
        plt.savefig(img_name)
        plt.close()
        print(f'已保存图片: {img_name}')
