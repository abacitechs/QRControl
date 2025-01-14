import os
import threading
import time

# Check if the application is running on a Raspberry Pi
is_raspberry = os.getenv('IS_RASPBERRY', 'false').lower() == 'true'

# Try importing RPi.GPIO only if running on a Raspberry Pi
if is_raspberry:
    try:
        import RPi.GPIO as GPIO
        GPIO_AVAILABLE = True
    except ImportError:
        GPIO_AVAILABLE = False
        print("RPi.GPIO library is not available. GPIO functionality will be disabled.")
else:
    GPIO_AVAILABLE = False
    print("Not running on a Raspberry Pi. GPIO functionality will be disabled.")

def toggle_gpio(gpio_pin):
    """
    Toggles a GPIO pin HIGH for 2 seconds and then LOW, with cleanup in the same function.
    This function works conditionally based on the availability of RPi.GPIO.

    Args:
        gpio_pin (int): The GPIO pin number (BCM numbering).
    """
    if not GPIO_AVAILABLE:
        print("GPIO functionality is not supported on this system. Skipping toggle for pin:", gpio_pin)
        return

    def control_pin():
        try:
            # Setup the GPIO pin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio_pin, GPIO.OUT)

            # Set GPIO pin HIGH
            GPIO.output(gpio_pin, GPIO.HIGH)
            print(f"GPIO {gpio_pin} is HIGH")
            time.sleep(2)  # Keep it HIGH for 2 seconds

            # Set GPIO pin LOW
            GPIO.output(gpio_pin, GPIO.LOW)
            print(f"GPIO {gpio_pin} is LOW")
        except Exception as e:
            print(f"Error controlling GPIO {gpio_pin}: {e}")
        finally:
            # Cleanup the GPIO pin
            GPIO.cleanup(gpio_pin)
            print(f"GPIO {gpio_pin} cleaned up")

    # Create and start a thread
    thread = threading.Thread(target=control_pin)
    thread.start()
    return thread
