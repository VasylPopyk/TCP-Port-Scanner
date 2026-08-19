import program  


def main():
    print("=" * 50)
    print("       INTERACTIVE PORT SCANNER LAUNCHER       ")
    print("=" * 50 + "\n")

    target_ip = (
        input("Enter target IP address [default: 127.0.0.1]: ").strip()
        or "127.0.0.1"
    )
    start_port = int(
        input("Enter start port [default: 1]: ").strip() or "1"
    )
    end_port = int(
        input("Enter end port [default: 254]: ").strip() or "254"
    )
    threads = int(
        input("Enter max threads [default: 50]: ").strip() or "50"
    )
    timeout = float(
        input("Enter timeout in seconds [default: 1.0]: ").strip() or "1.0"
    )

    print("\n[*] Passing arguments directly to program.py...\n")

    try:
        program.run_scanner(
            host=target_ip,
            start_port=start_port,
            end_port=end_port,
            timeout=timeout,
            max_threads=threads,
        )
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")


if __name__ == "__main__":
    main()