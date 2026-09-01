# Decoder protocols 

RCHourglass can use different protocols to send passages information to the lap timing software:

* Cano/Cano classic protocol derived from original Cano decoder

* RCHourglass protocol, similar to Cano protocol, but passage informations have some extra info like number of hits/quality/voltage/temp

* AMBRc serial protocol 

* Tranx serial protocol

# Passage record format 

Passage information is sent as lines ended by Carriage Return and Line Feed.

The CANO protocol passage record is 14 characters long in the format 

**nnnnnntttttttt**

* **nnnnnn** is an ASCII HEX string that represents the transponder number.

* **tttttttt** part is an 8 character ASCII string representing the passage time in 
quarters of milliseconds from decoder startup.


Example record

**23E35500075A06**

Transponder: *0x23E355* = *2351957*

Time in quarter of ms  = *0x00075A06*  = *120.449 seconds*



The RCHourglass protocol passage record is 25 characters long in the format 

**nnnnnntttttttt-idhhqqvvtm**

The first 14 characters are the same as Cano protocol.

* **id**  the decoder ID (part of the decoder setup)
* **hh**  the number of hits received from the transponder
* **qq**  quality indicator of read (0-100%). 
* **vv**  voltage in 1/10 of V
* **tt**  temperature (+100 °C offset)

All numbers a ASCII Hex.

Example record

**23E35500075A06-01152A3787**

Transponder: **0x23E355** = **2351957**

Time in quarter of ms  = **0x00075A06**  = **120.449 seconds**

Decoder ID : **0x01**

Hits : **0x15 = 21 hits**

Quality : **0x2A = 52%**

Voltage: **0x37   = 5.5V**

Temperature: **0x87 - 100 = 35°C** 


**NOTE** Temperature and voltage info are read only from RCHouglass transponder firmware to be developed. Values are 0 for measure not available.


# Decoder ports

RCHourglass decoder has two serial ports. One is USB-emulated, the other is on PSOC pins 12[6] and 12[7].

Each serial port can be configured to use a different protocol emulation. 

The second serial port is available also as a USB emulated COM through the KitProg half of the development board, 
and can be used to interface other hardware without USB ports/drivers. 

**The default startup status of the serial port is OFF, and can be changed with RCHourglass Manager.**

**Serial port (not USB) uses 57600 8,N,1 data rate.**

**NOTE** If decoder is to be used only with an embedded serial hardware connection to  pins 12[6] and 12[7], for best performances it's better to set USB power on mode to OFF.