#!/usr/bin/env python3
"""
Loading Spinner for CLI Tools

ASCII spinner animation for CLI tools. Provides visual feedback during long operations.
Auto-detects TTY and falls back to simple text when output is piped.

Usage:
    from spinner import Spinner

    spinner = Spinner("Loading data")
    spinner.start()
    # ... do work ...
    spinner.stop()
"""

import sys
import threading
import time


class Spinner:
    """ASCII loading spinner for CLI operations."""

    def __init__(self, message="Loading"):
        """
        Initialize the spinner.

        Args:
            message: Text to display alongside the spinner
        """
        self.spinner_cycle = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.stop_running = threading.Event()
        self.spin_thread = None
        self.message = message
        # Auto-detect if output is a TTY (not piped)
        self.is_tty = sys.stdout.isatty()

    def start(self):
        """Start the spinner in a separate thread."""
        if not self.is_tty:
            # If output is piped, just print the message once
            print(f"{self.message}...")
            return

        self.stop_running.clear()
        self.spin_thread = threading.Thread(target=self._spin)
        self.spin_thread.daemon = True
        self.spin_thread.start()

    def _spin(self):
        """The spinning animation loop."""
        i = 0
        while not self.stop_running.is_set():
            sys.stdout.write(f'\r{self.spinner_cycle[i % len(self.spinner_cycle)]} {self.message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def stop(self):
        """Stop the spinner and clear the line."""
        if not self.is_tty:
            return

        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            sys.stdout.flush()


# Alternative spinner styles
SPINNER_STYLES = {
    'braille': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    'classic': ['|', '/', '-', '\\'],
    'dots': ['.  ', '.. ', '...', ' ..', '  .', '   '],
    'arrows': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
    'bar': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
}


class StyledSpinner(Spinner):
    """Spinner with customizable styles."""

    def __init__(self, message="Loading", style="braille"):
        """
        Initialize spinner with a specific style.

        Args:
            message: Text to display alongside the spinner
            style: One of 'braille', 'classic', 'dots', 'arrows', 'bar'
        """
        super().__init__(message)
        self.spinner_cycle = SPINNER_STYLES.get(style, SPINNER_STYLES['braille'])


if __name__ == "__main__":
    # Demo all spinner styles
    for style_name in SPINNER_STYLES:
        spinner = StyledSpinner(f"Testing {style_name} style", style=style_name)
        spinner.start()
        time.sleep(2)
        spinner.stop()
        print(f"✓ {style_name} complete")
