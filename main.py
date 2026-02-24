from core.agent import StryxCore

def main():
    system = StryxCore()

    while True:
        task = input("STRYX > ")

        if task.lower() == "exit":
            print("Shutting down STRYX...")
            break

        if task.lower() == "help":
            print("Commands: report topic, summary text, exit\n")
            continue

        result = system.process(task)
        print(f"→ {result}\n")

if __name__ == "__main__":
    main()