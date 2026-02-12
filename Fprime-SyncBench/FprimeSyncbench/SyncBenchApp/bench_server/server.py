import time
import csv
import socket

number_of_runs = 35
tlm_channel_name = "FprimeSyncbench.syncBench.TelemtrySender"
evt_name = "FprimeSyncbench.syncBench.EventSender"
fieldnames = ["sequence", "transport_type", "fsw_timestamp_sec", "arrival_timestamp_sec", "latency_ms"]

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('localhost', 10000)

def test_benchmark_telemetry(fprime_test_api):
    results_buffer = []
    fprime_test_api.clear_histories()

    fprime_test_api.send_command("FprimeSyncbench.syncBench.BENCH_TLM", [number_of_runs])

    for i in range(number_of_runs):
        result = fprime_test_api.await_telemetry(tlm_channel_name)
        arrival_time = time.time()

        val = result.get_val()
        fsw_time_usecs = int(val["timestamp"])
        fsw_time_secs = fsw_time_usecs / 1000000.0

        results_buffer.append({
            "sequence": val["sequence_num"],
            "transport_type": val["transport_type"],
            "fsw_timestamp_sec": fsw_time_secs,
            "arrival_timestamp_sec": arrival_time,
            # (Arrival in sec - Departure in sec) * 1000 - Latency in Milliseconds
            "latency_ms": (arrival_time - fsw_time_secs) * 1000
        })


    with open("tlm_bench_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_buffer)

    assert len(results_buffer) == number_of_runs

def test_benchmark_events(fprime_test_api):
    results_buffer = []
    fprime_test_api.clear_histories()

    fprime_test_api.send_command("FprimeSyncbench.syncBench.BENCH_EVT", [number_of_runs])

    for i in range(number_of_runs):
        result = fprime_test_api.await_event(evt_name)
        arrival_time = time.time()

        args = result.get_args()
        bench_data_obj = args[0]

        data_values = bench_data_obj.val

        fsw_time_usecs = int(data_values["timestamp"])
        fsw_time_secs = fsw_time_usecs / 1000000.0

        results_buffer.append({
            "sequence": data_values["sequence_num"],
            "transport_type": data_values["transport_type"],
            "fsw_timestamp_sec": fsw_time_secs,
            "arrival_timestamp_sec": arrival_time,
            # (Arrival in sec - Departure in sec) * 1000 - Latency in Milliseconds
            "latency_ms": (arrival_time - fsw_time_secs) * 1000
        })


    with open("evt_bench_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_buffer)

    assert len(results_buffer) == number_of_runs


def test_buffer_connection(fprime_test_api):
    results_buffer = []
    fprime_test_api.clear_histories()

    fprime_test_api.send_command("FprimeSyncbench.syncBench.BENCH_BUF", [number_of_runs])


def start_buffer_server():
    print("Starting server")
    socket.bind(server_addr)
    socket.listen(1)

    while True:
        print("waiting for connetion")
        connection, client_addr = socket.accept()
        try:
            print("Connection from ", client_addr)
            while True:
                data = connection.recv(16)
                if data:

                else:
                    break
        finally:
            connection.close()


def benchmark_telemetry_chnl_time(fprime_test_api):
    # This is only testing the time it takes for fprime to move data from tlmWrite to Svc.TlmChan ( which is the telemetry database, so its negligble)
    number_of_runs = 35
    channel = "FprimeSyncbench.syncBench.TelemtrySender"

    telem_seq = [channel] * number_of_runs

    fprime_test_api.clear_histories()

    results =  fprime_test_api.send_and_await_telemetry("FprimeSyncbench.syncBench.BENCH_TLM", [number_of_runs], telem_seq, timeout=10)

    results_buffer = []
    for entry in results:

        time_obj = entry.get_time()
        arrival_time = time_obj.seconds + (time_obj.useconds / 1000000.0)

        val = entry.get_val()
        fsw_time_usecs = int(val["timestamp"])
        fsw_time_secs = fsw_time_usecs / 1000000.0

        results_buffer.append({
            "sequence": val["sequence_num"],
            "transport_type": val["transport_type"],
            "fsw_timestamp_sec": fsw_time_secs,
            "arrival_timestamp_sec": arrival_time,
            # (Arrival in sec - Departure in sec) * 1000 - Latency in Milliseconds
            "latency_ms": (arrival_time - fsw_time_secs) * 1000
        })

    with open("benchmark_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_buffer)

    print(f"Benchmark Complete. Captured {len(results)} packets.")
