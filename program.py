import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host: str, port: int, timeout: float) -> tuple[int, bool, str]:
    """Attempts connection to host:port and retrieves service banner."""
    banner = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            if s.connect_ex((host, port)) == 0:
                try:
                    s.sendall(b"\r\n")
                    data = s.recv(1024)
                    banner = data.decode(errors="ignore").strip()
                except (socket.timeout, OSError):
                    banner = "No banner returned"

                return (port, True, banner)
        except OSError:
            pass

    return (port, False, banner)


def run_scanner(
    host: str, start_port: int, end_port: int, timeout: float, max_threads: int
) -> None:
    """Executes concurrent port scanning across the specified port range."""
    ports = range(start_port, end_port + 1)
    print(f"[*] Starting scan on target: {host}")
    print(f"[*] Scanning ports {start_port} through {end_port}...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all tasks to the thread pool
        futures = {
            executor.submit(scan_port, host, port, timeout): port for port in ports
        }

        for future in as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                open_ports.append(port)
                display_banner = banner if banner else "N/A"
                print(f"[+] Port {port:<5} OPEN | Banner: {display_banner}")

    print(
        f"\n[*] Scan complete. Found {len(open_ports)} open port(s) on {host}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-threaded TCP Banner Grabber & Port Scanner",
        epilog="Example: python scanner.py 127.0.0.1 --start-port 1 --end-port 1024",
    )

    parser.add_argument(
        "ip",
        type=str,
        nargs="?",
        default="127.0.0.1",
        help="Target IP address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Max worker threads (default: 50)",
    )
    parser.add_argument(
        "--start-port", type=int, default=1, help="Starting port (default: 1)"
    )
    parser.add_argument(
        "--end-port",
        type=int,
        default=254,
        help="Ending port (default: 254)",
    )

    args = parser.parse_args()

    run_scanner(
        args.ip, args.start_port, args.end_port, args.timeout, args.threads
    )


if __name__ == "__main__":
    main()