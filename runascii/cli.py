from time import sleep

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

    # TODO Add GPU metrics
    report = f"C{cpu_util:02} M{mem_percent:02} U{upload_speed:02} D{download_speed:02}"
    print(report)


if __name__ == "__main__":
    main()
