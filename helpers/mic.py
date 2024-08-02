import pyaudio

def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    default_device_index = p.get_default_input_device_info().get('index')
    default_device_name = p.get_device_info_by_index(default_device_index).get('name')

    print(f"{default_device_index}: - {default_device_name}")

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0 and i != default_device_index:
            print(f"{i}: - {device_info.get('name')}")
    p.terminate()

def get_device_index(num_devices):
    while True:
        user_input = input("Enter the Input Device id you want to use (default is 1): ").strip()
        if user_input == "":
            return 1  # Default to 1 if no input is given
        if user_input.isdigit():
            device_index = int(user_input)
            if 0 <= device_index < num_devices:
                return device_index
        print("Invalid input. Please enter a valid number.")