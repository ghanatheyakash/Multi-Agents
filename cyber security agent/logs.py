import win32evtlog
import csv

def fetch_windows_logs(log_types=None):
    if log_types is None:
        log_types = ["Application", "Security", "System", "Setup", "ForwardedEvents"]
    
    for log_type in log_types:
        logs = []
        output_file = f"{log_type}_logs.csv"
        
        try:
            hand = win32evtlog.OpenEventLog(None, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            total_records = win32evtlog.GetNumberOfEventLogRecords(hand)
            
            while True:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                if not events:
                    break
                for event in events:
                    logs.append([event.TimeGenerated, event.EventID, event.SourceName, event.StringInserts])
        
        except Exception as e:
            print(f"Failed to read {log_type} logs: {e}")
            continue
        
        # Save logs to CSV
        with open(output_file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "EventID", "Source", "Details"])
            for log in logs:
                writer.writerow([log[0], log[1], log[2], log[3] if log[3] else "N/A"])
        
        print(f"Logs saved to {output_file}")

# Run the function to fetch logs from all specified types
fetch_windows_logs()
