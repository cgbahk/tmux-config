import sys
from time import sleep
import shutil
import subprocess

import psutil

INTERVAL = 0.4  # seconds


def main():
    # TODO Use thread to measure each metric
    cpu_utils = psutil.cpu_percent(interval=INTERVAL, percpu=True)
    cpu_util = int(sum(cpu_utils) / len(cpu_utils))

    mem_percent = int(psutil.virtual_memory().percent)

    net_stat_0 = psutil.net_io_counters()
    sleep(INTERVAL)
    net_stat_1 = psutil.net_io_counters()

    # In MiB unit
    download_speed = int((net_stat_1.bytes_recv - net_stat_0.bytes_recv) / 1024**2 / INTERVAL)
    upload_speed = int((net_stat_1.bytes_sent - net_stat_0.bytes_sent) / 1024**2 / INTERVAL)

    report = f"C{cpu_util:02} M{mem_percent:02} U{upload_speed:02} D{download_speed:02}"

    if shutil.which("nvidia-smi") is None:
        print(report)
        sys.exit()

    result = subprocess.check_output(
        [
            "nvidia-smi",
            "--format=csv,noheader,nounits",
            #            0               1           2            3          4
            "--query-gpu=utilization.gpu,memory.free,memory.total,power.draw,power.limit",
        ]
    ).decode().strip()

    for per_gpu_result in result.split("\n"):
        info = per_gpu_result.split(",")
        gpu_util = int(info[0])
        gpu_mem_percent = int(100 - float(info[1]) * 100 / float(info[2]))
        gpu_pow_percent = int(float(info[3]) * 100 / float(info[4]))

        report += f" G{gpu_util:02} M{gpu_mem_percent:02} P{gpu_pow_percent:02}"

    print(report)


if __name__ == "__main__":
    main()
