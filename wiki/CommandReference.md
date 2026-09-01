# Decoder commands/operations

RCHourglass decoder can execute commands. A software configurator called RCHourglassManager is available for download here.
The source of RCHourglassManager can be used as a starting point to port to other platform or to study the protocol.

To issue manual commands, a terminal program like PUTTY or Hyperterm can be used to connect to the COM port. 
**NOTE**: manual command does not have any feedback while typing, so you might want to type 'blind' or enable feedback in terminal options.
When **ENTER** is hit, the command is executed. 

Most of the commands respond with a line that starts with **SUCCESS** or **ERROR**
Some commands (like transponder info) have multiple lines response closed by a **SUCCESS** line.  
 
# VERSION and LICENSE commands

|**Command**|**Description**|**Note**|
|-----------|---------------|--------|
|**VERSION**|Returns the current firmware version. |Example: RC Hourglass v0.5 beta|
|**LICENSE**|Returns the licensing terms. |Multi line response. Last line contains 'Marco Venturini'|

**Note that any derivative work **MUST** respond to LICENSE command with the same licensing terms.**

# Mode setup commands

The mode setup commands will make the decoder change the emulation mode of the current port until power off.
These commands respond with an echo of the mode set (not a SUCCESS response)


|**Command**|**Description**|
|-----------|---------------|
|**RCHOURGLASS MODE**| Extended Cano mode with hits, voltage, quality and temp reporting|
|**CANO MODE**| The decoder works in CANO emulation mode **with** decode of transponder number|
|**CANO CLASSIC MODE**| The decoder works in CANO emulation mode **without** decode of transponder number|
|**AMBRC MODE**| Emulation for AMBRC protocol. |
|**MONITOR MODE**|writes to serial *every* packet read by the loop, without any decoding. Useful to check circuit performance/issues.|
|**TRANX MODE**| Emulation of TranX protocol|
|**LOOPBACK MODE**| All traffic from the other serial is loopbacked here with character < for incoming messages and > for outgoing messages|


**NOTE for AMB emulation** this is an *emulation* for AMBRC protocol. Passage records with number of hits and low voltage indicator are supported. 
 This is to use the decoder with lap timing softwares that do not support CANO protocol. Low voltage bit is rised with a voltage threshold set in the 
 decoder configuration
 
 
 # Startup mode setup commands
 
 This command set the startup emulation mode for the two serial ports (USB and serial)
 
|**Command**|**Description**|
|-----------|---------------|
|**SET SERIAL [CANO : CANO CLASSIC : RCHOURGLASS : TRANX : AMBRC : OFF]**| Set power on mode for the serial port|
|**SET USB [CANO : CANO CLASSIC : RCHOURGLASS : TRANX : AMBRC : OFF]**| Set power on mode for the USB port|
|**GET SERIAL**| Returns startup serial mode: SUCCESS GET SERIAL [mode] |
|**GET USB**| Returns startup USB mode: SUCCESS GET SERIAL [mode] |


# Time commands
 
|**Command**|**Description**|  
|-----------|---------------| 
|**GET TIME**| Return the curent time of the decoder in quarters of ms|
|**SET TIME [t]**| Sets the curent time of the decoder in quarters of ms. [t] is in hex|

Example:
 
**GET TIME**
 
Response
 
**SUCCESS GET TIME 00075A06** 
 
Current time in quarter of ms  = **0x00075A06**  = **120.449 seconds**
 
To set the same time:

**SET TIME 75A06** 
 
# Transponder management

The RC4 transponders can be detected only after they've been registered in the decoder memory. RC4 Hybrid should not need registration.

As for version Beta 3, a maximum of 40 transponders can be kept in the memory and persist even in case of power disconnection.

## How to register RC4 transponder

Place and stop the car above the wire. 

The blue LED on the PSOC board should be well lit.

Avoid any other car passage. Issue the command **REGISTER _tx number_**, for example **REGISTER 3462137**

The decoder will start learn and return success or failure. In case of failure, reposition the car and/or check correct loop connection. 

In case of success, the 12 most important 'packets' of the transponder are reported, with the number of hits for each one.

A minimum number of hits above 30, with the maximum above 100 is a very good target. 

The registration can use a nickname for the transponder, like **REGISTER 3462137 MARCO**. The nick name will appear in the list of registered transponders.

The last option is to make a transponder 'important' that is it's never going to be 'kicked out' of the memory if the limit of 40 transponders is reached.

Important transponders can be only deleted manually. When the memory is full, the oldest non important transponders are deleted to make room for the last registered one.

For example, to register yours as an important transponder, write **REGISTER I 3462137 MINE** where MINE is the optional nickname.

Learn process can be interrupted with the **ABORT** command, but it will  timeout if no transponder is detected.

The **LIST** command will show the registered transponders.

The **DELETE _tx number_**, for example **DELETE 3462137**, will remove a transponder registration from the decoder memory.

The **INFO _tx number_**,  will show registration informations for a specific transponder. 

This commands are made to backup on the computer registration informations.

**Flashing a new firmware will EREASE the registrations done.**

# Configuration, beeper and led management

|**Command**|**Description**|  
|-----------|---------------| 
| **GET LED** | Returns SUCCESS LED [duration]|
| **SET LED** [0-255]|Sets led  notification in ms when passage is detected. Duration 0 = no led notification.|
| **GET BEEPER** | Returns SUCCESS BEEP [duration] [divider]|
| **BEEP** | Emit a beep|
| **SET BEEP** [0-255] [0 or 6-30] |Set beep  notification in ms when passage is detected. Duration 0 = no beep notification. Divider sets beeper frequency: 0 is only pulse, otherwise frequency is 20kHz/divider, where divider must be *between 6 and 30*|
| **GET ID** |Returns SUCCESS GET ID [0-255]|
| **SET ID** [0-255]|Sets decoder ID|
| **GET VMIN** |Returns SUCCESS GET VMIN [0-255] where the number is voltage threshold in 1/10 of volts|
| **SET VMIN** [0-255]|Set the voltage threshold to actiate low battery warning voltage is value divided by 10. 0 = no warning. Max Voltage = 25.5V|

 

**NOTE** a 50 ms blank time is always inserted in case of multiple close car passages.

# PIC programming commands

This commands require the optional components of the schematic to allow direct PIC programming.

**WARNING** Do NOT connect unsupported PIC models or LF PIC models. The voltage might destroy the component.


|**Command**|**Description**| 
|-----------|---------------| 
|**DETECT**| Returns the model ID of pic in the programming socket|
|**BEGIN PROGRAMMING**|Begin PIC programming|
|**ERASE DEVICE**|Erase pic in socket. Must be in program mode|
|**WRITEMEM [V] <ADDRESS> <DATA>**| Write PIC memory at given address. [V] option is to verify written data. Address is in HEX ASCII. The Data is expressed as sequence of max 10 words each one expressed with 4 ASCII character. PIC programming must be started before writing memory|
|**END PROGRAMMING**|End PIC program mode|
|**ABORT**|Ends programming or RC4 learn|

 
DETECT response is multi line. The last line is **SUCCESS PIC MODEL NNNN**  where **NNNN* is Hex part number ID. A value of 3066 sould be reported for PIC 16F18313.



 


