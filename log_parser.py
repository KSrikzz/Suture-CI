import re

class LogParser:
    def __init__(self):
        self.error_keywords = ["ERROR", "FATAL", "Exception", "Traceback", "panic:", "Error:"]

    def extract_error_context(self, raw_logs, context_lines=15):
        """
        Scans raw logs for errors and returns a focused chunk of context.
        context_lines: How many lines to capture after the error is found.
        """
        log_lines = raw_logs.strip().split('\n')
        error_blocks = []
        
        for i, line in enumerate(log_lines):
            if any(keyword.lower() in line.lower() for keyword in self.error_keywords):
                start_index = max(0, i - 3)
                end_index = min(len(log_lines), i + context_lines)
                context_block = "\n".join(log_lines[start_index:end_index])
                if context_block not in error_blocks:
                    error_blocks.append(context_block)
        
        return error_blocks
if __name__ == "__main__":
    parser = LogParser()

    dummy_logs = """
    INFO: Starting server on port 8080
    INFO: User authentication successful
    WARN: Deprecated API call detected
    INFO: Processing payment for order #9942
    ERROR: Payment processing failed
    Traceback (most recent call last):
      File "payment_gateway.py", line 42, in process_payment
        charge_credit_card(user_id, amount)
      File "stripe_api.py", line 12, in charge_credit_card
        raise ConnectionError("Timeout connecting to payment provider")
    ConnectionError: Timeout connecting to payment provider
    INFO: Retrying connection...
    """

    print("[*] Scanning logs for errors...")
    found_errors = parser.extract_error_context(dummy_logs)
    
    if found_errors:
        print(f"[+] Found {len(found_errors)} error block(s). Context extracted:\n")
        for i, error in enumerate(found_errors):
            print(f"--- Error Block {i+1} ---")
            print(error)
            print("-----------------------\n")
    else:
        print("[-] No errors detected in logs.")