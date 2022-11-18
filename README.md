# Renogy WiFi
Renogy RS232 WiFi adapter and display module

### What is it?

A compact WiFi adapter and remote monitoring display for Renogy¹ brand charge controllers. It has been tested with Renogy Rover / Adventurer / Wanderer series controllers, it does not support Rover Elite series. However it might work with other 'SRNE' compatible RS232 devices like Rich Solar.

### Configuration
- Press BOOTSEL button and copy the firmware `uf2` file to Pico W as mentioned in [drag-and-drop-micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython)
- Download thonny editor ([thonny.org](https://thonny.org/))
- Download this repo source code and modify values in `Device.py`
- Upload the entire code to your Pico W using Thonny editor (Do not press BOOTSEL now, [read more](https://www.electromaker.io/blog/article/electromaker-educator-getting-started-with-the-pico-w)) 

<img width="700px" src="https://user-images.githubusercontent.com/111796612/202618561-c0973ac7-efcb-4c31-af6c-e20cfc7628ea.png" />

Now your WiFi module is ready, just connect it to your Charge Controller using RJ12 cable. Check [Wiki](https://github.com/thewestlabs/renogy-wifi/wiki) for more details on hardware and schematics.

### References
- Modbus library is based on [pycom/pycom-modbus](https://github.com/pycom/pycom-modbus/)
- Renogy library is based on [corbinbs/solarshed](https://github.com/corbinbs/solarshed)
