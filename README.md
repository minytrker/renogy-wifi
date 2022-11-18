# renogy-wifi
Renogy RS232 WiFi adapter and display module

### What is it?

a compact WiFi adapter and remote monitoring display for Renogy¹ brand charge controllers. It has been tested with Renogy Rover / Adventurer / Wanderer series controllers, it does not support Rover Elite series. However it might work with other 'SRNE' compatible RS232 devices like Rich Solar.

### How to configure?
- Press BOOTSEL  button and flash the Pico W firmware with uf2 file as mentioned in [drag-and-drop-micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython)
- Download thonny editor ([thonny.org](https://thonny.org/))
- Download this source repo and modify values in `Device.py`
- Upload the code to your Pico W using Thonny editor (Do not press BOOTSEL now, [read more](https://www.electromaker.io/blog/article/electromaker-educator-getting-started-with-the-pico-w)) 

<img width="700px" src="https://user-images.githubusercontent.com/111796612/202618561-c0973ac7-efcb-4c31-af6c-e20cfc7628ea.png" />



### What's included?
- Fully assembled PCB with MAX3232 chip and RJ12 connector
- Raspberry Pico W (add-on)
- 0.91" OLED display (add-on, optional)

### References
- Modbus library is based on [pycom/pycom-modbus](https://github.com/pycom/pycom-modbus/)
- Renogy library is based on [corbinbs/solarshed](https://github.com/corbinbs/solarshed)
