import argparse
import numpy as np
import time, random, string, signal, sys
from camera import Camera
from benchmark import Benchmark

def make_scene():
    return "benchmark_"+"".join(random.choice(string.ascii_lowercase+string.digits) for i in range(5))

def main(max_cams, timeout, broker, port, name, interval):
    avg_lats = []
    bpms_sent = []
    bpms_recvd = []
    dropped_clients = []
    dropped_packets_percent = []
    cpu = []
    mem = []
    for num_cams in range(1, max_cams+interval, interval):
        print(f"----- Running Benchmark with {num_cams} Clients -----")

        test = Benchmark(f"{name}_c{num_cams}", num_cams, timeout*60000, broker, port, make_scene())
        test.run()

        avg_lats += [test.get_avg_lats() if test.get_avg_lats() else [-1] * 100]
        bpms_sent += [test.get_bpms_sent()]
        bpms_recvd += [test.get_bpms_recvd()]
        dropped_clients += [test.get_dropped_clients()]
        dropped_packets_percent += [test.dropped_packets_percent()]
        cpu += [np.mean(test.get_cpu())]
        mem += [np.mean(test.get_mem())]

        print("----- Summary -----")
        print(f"{num_cams} Clients connecting to {broker}:{port} with {timeout} sec timeout:")
        print(f"{np.mean(avg_lats[-1])} ms | {bpms_sent[-1]} bytes/ms sent | {bpms_recvd[-1]} bytes/ms received")
        print(f"{dropped_clients[-1]} clients dropped | {dropped_packets_percent[-1]}% packet loss | {cpu[-1]}% cpu usage | {mem[-1]}% mem usage")
        print()

        test.save()

        time.sleep(1)

    avg_lats = np.array(avg_lats)
    bpms_sent = np.array(bpms_sent)
    bpms_recvd = np.array(bpms_recvd)
    dropped_clients = np.array(dropped_clients)
    dropped_packets_percent = np.array(dropped_packets_percent)
    cpu = np.array(cpu)
    mem = np.array(mem)

    np.savez(f"data/benchmark_{name}_c{num_cams}_i{interval}",
                avg_lats=avg_lats,
                bpms_sent=bpms_sent, bpms_recvd=bpms_recvd,
                dropped_clients=dropped_clients, dropped_packets_percent=dropped_packets_percent,
                cpu=cpu, mem=mem)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("ARENA MQTT broker benchmarking"))
    parser.add_argument("-c", "--max_cams", type=int, help="Number of clients to spawn",
                        default=1)
    parser.add_argument("-b", "--broker", type=str, help="Broker to connect to",
                        default="oz.andrew.cmu.edu")
    parser.add_argument("-p", "--port", type=int, help="Port to connect to",
                        default=9001)
    parser.add_argument("-n", "--name", type=str, help="Optional name for saved plot",
                        default="benchmark")
    parser.add_argument("-t", "--timeout", type=float, help="Amount of mins to wait before ending data collection",
                        default=3.0) # default is 3 mins
    parser.add_argument("-i", "--interval", type=int, help="Interval of clients for benchmarking",
                        default=1)
    args = parser.parse_args()

    main(**vars(args))
