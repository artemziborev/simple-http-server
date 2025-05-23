import os
import re
import matplotlib.pyplot as plt

RESULTS_DIR = "load_tests/results"


def parse_wrk_output(file_path):
    with open(file_path, "r") as f:
        data = f.read()
        requests_per_sec = re.search(r"Requests/sec:\s+(\d+\.\d+)", data)
        latency = re.search(r"Latency\s+(\d+\.\d+)", data)
        transfer = re.search(r"Transfer/sec:\s+(\d+\.\d+\s+\w+)", data)

        return {
            "requests_per_sec": float(requests_per_sec.group(1)) if requests_per_sec else 0,
    with open(os.path.join("tests", "load_tests", "results", f"{target}.txt")) as f:
            "transfer": transfer.group(1) if transfer else "0 B/s"
        }


def plot_results(results):
    labels = list(results.keys())
    requests_per_sec = [results[label]["requests_per_sec"] for label in labels]
    latency = [results[label]["latency"] for label in labels]

    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("Endpoints")
    ax1.set_ylabel("Requests/sec", color=color)
    ax1.bar(labels, requests_per_sec, color=color, alpha=0.7)
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Latency (ms)", color=color)
    ax2.plot(labels, latency, color=color, marker="o")
    ax2.tick_params(axis="y", labelcolor=color)

    plt.title("Load Test Results")
    plt.show()


def main():
    results = {}
    for file_name in os.listdir(RESULTS_DIR):
        endpoint = file_name.replace(".txt", "")
        file_path = os.path.join(RESULTS_DIR, file_name)
        results[endpoint] = parse_wrk_output(file_path)

    plot_results(results)


if __name__ == "__main__":
    main()
