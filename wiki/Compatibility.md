# Decoder and transponder compatibility chart

Transponder and decoder compatibility chart.

| *Decoder* | *RCHourglass transponder*    | *Cano* | *AMBRc/Dp* | *RC4* | *RC4 Hybrid* | *MRT* | *ATTINY 25* |
|-----------|:----------------:|:------:|:----------:|:-----:|:------------:|:-----:|:-----------:|
|RCHourglass decoder v0.5|*|*|*|*(1)|*(2)|*|*|
|Cano decoder|*|*|*|||*|?|
|RC3 decoder|*(3)|*|*|||*|?|
|MyLaps RC4 < v4.5|*(3)||*|*|*|*|?|
|MyLaps RC4 >= v4.5||||*|*|||
 
 *Note 1*: Pure RC4 transponders need to be learned by RCHourglass decoder to be detected.
 Learning is done with *RCHourglass Manager* software, and internal memory stores up to 40 transponders.
 The memory is mantained at power off of the decoder.
 
 *Note 2*: Hybrid RC4 transponders can be learned by RCHourglass decoder to be detected, but work also 
 without the learn process. Learning them should increase passsage detection sensitivity.

 *Note 3*: The compatibility is tested with the 11 transponder numbers of the official RCHourglass transponder firmware.
 With the *RCHourglass Manager* software it is possible to tweak the firmware to create new numbers.
 Some 'tweaked' numbers work also on Mylaps decoder, but not all.

 
# Software compatibility chart

These lap timing software have been tested with RCHourglass decoder.


| *Software* | *Cano Mode*    | *AMBRc Mode* | *TranX Mode* | *Notes* |
|--------|:------------:|:---------:|:----------:|------|
|ZRound|*|*|||
|FlipSide|*|*||(1)|
|Alycat v.9| |*|||
|LapsFree| |*|||
|RCTiming 6.3| |*|||
|Rentix| ||*||
|Everlaps| |*||(2)|
 
 *Note 1*: Tested with version 13.3.0.23 supplied in Howard Cano ZIP
 
 *Note 2*: Make sure to lower the minimum signal threshold in decoder setup 
 
 **SETUP HINTS** Some (older) software support only COM ports from 1 to 4.

The USB serial port number can be changed in windows setup.

* Open *device manager* 
* right click on the serial port under *Ports (COM LPT)* > *Properties.*
* Go to the *Port Settings* tab and click *Advanced...*. 
* Select the COM port in the drop down menu.

**It seems that access to the lower number COM Ports requires running the software as administrator. 
 This applies also to *RCHourglass Manager*.**