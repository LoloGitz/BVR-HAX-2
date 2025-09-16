import time
import sys

def clear_last_line():
    """Moves the cursor up one line and clears it."""
    # Cursor up one line (`\x1b[1A`) and clear line (`\x1b[2K`)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def clear_from_cursor_to_end_of_line():
    """Clears text from the current cursor position to the end of the line."""
    sys.stdout.write('\x1b[0K')

def overwrite_line_example():
    print("Starting process...")
    for i in range(10):
        # The `end='\r'` moves the cursor back to the start of the line
        print(f"Progress: {i * 10}%", end='\r')
        time.sleep(0.5)
    print("Progress: 100%") # Overwrites the last line fully
    print("Process finished.")

def update_multiple_lines_example():
    print("Status 1: pending")
    print("Status 2: pending")
    print("Status 3: pending")
    time.sleep(1)

    # Update line 2: Move cursor up, clear line, and print new text
    sys.stdout.write('\x1b[2A') # Move cursor up two lines
    sys.stdout.write('\x1b[2K') # Clear the current (middle) line
    print("Status 2: completed")
    sys.stdout.flush() # Ensure the output is immediately shown
    time.sleep(1)

    # Update line 1: Move cursor up, clear line, and print new text
    sys.stdout.write('\x1b[3A') # Move cursor up three lines
    sys.stdout.write('\x1b[2K') # Clear the current (top) line
    print("Status 1: completed")
    sys.stdout.flush()
    time.sleep(1)

    # Return cursor to bottom and print completion message
    print("\n\nAll processes completed.")

overwrite_line_example()
print("\n--- Next Example ---\n")
update_multiple_lines_example()
