# Renogy WiFi
Renogy RS232 WiFi adapter and display module

### What is it?

A compact WiFi adapter and remote monitoring display for Renogy brand charge controllers. It has been tested with Renogy Rover / Adventurer / Wanderer series controllers, it does not support Rover Elite series. However it might work with other 'SRNE' compatible RS232 devices like Rich Solar.

### Configuration
- Connect Pico W to your laptop while pressing BOOTSEL button and copy the firmware [uf2](https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2) file to Pico ([read more](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython))
- Download thonny editor ([thonny.org](https://thonny.org/))
- Download `renogy-wifi` source code (this repo) and modify values in `Device.py`
- Upload the entire code to your Pico W using Thonny editor (Do not press BOOTSEL now, [read more](https://www.electromaker.io/blog/article/electromaker-educator-getting-started-with-the-pico-w)) 

<img width="700px" src="https://user-images.githubusercontent.com/111796612/202618561-c0973ac7-efcb-4c31-af6c-e20cfc7628ea.png" />

Your WiFi module is now ready to deploy, just connect it to your Renogy charge controller using RJ12 cable. Check [Wiki](https://github.com/thewestlabs/renogy-wifi/wiki) for more details on hardware and schematics.

### References
- Modbus library is based on [pycom/pycom-modbus](https://github.com/pycom/pycom-modbus/)
- Renogy library is based on [corbinbs/solarshed](https://github.com/corbinbs/solarshed)

### How to buy
<a href="https://www.tindie.com/stores/westlabs/?ref=offsite_badges&utm_source=sellers_cyrils&utm_medium=badges&utm_campaign=badge_medium"><img src="https://d2ss6ovg47m0r5.cloudfront.net/badges/tindie-mediums.png" alt="I sell on Tindie" width="150" height="78"></a>

https://www.tindie.com/products/27955/
