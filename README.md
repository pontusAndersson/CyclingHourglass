# CyclingHourglass
DIY lap timing system. 



# What is it?
Cycling Hourglass is a project to develop a DIY automatic timing system that can be used in cycling racing.
It is a development much based on RC hourglass.
The focus of the project is hardware design of the pieces of the system. 
The hardware is compatible with existing lap timing software.The project idea comes from two threads in RCTech.net forums about 
lap timing devices design by Howard Cano.The scope of the project is to simplify the design, document the building process and 
add new features.

Have fun, and donate to a childer charity (see license) 

Pontus



# Project status

Transponder and decoder build instructions are published in the wiki.

The project is in beta status as features are added/tested. Several working prototypes of the decoder have been tested succesfully. 
Many transponder prototypes have been tested successfully. 

RCHourglass Manager software is available for decoder configuration and RC4 transponder detection



# Compatibility

Check the Compatibility chart in the Wiki for more details.

The RCHourglass transponder should work with CANO decoder and AMB/Mylaps decoders unless they're updated to the latest firmware.

The decoder can detect RCHourlass, AMB, MRT, CANO and RC3 transponders. RC4 transponders can be detected after registration in the decoder memory.

The decoder is compatible with lap timing software using the CANO protocol (Z-Round and Flipside racing) and serial AmbRc (most of the timing software support this protocol).

# Related software

[LAPS](https://github.com/snowblind/LAPS) is a Node.js web app for showing lap data from RC Hourglass decoder hardware. Logo use by permission of Marco Venturini (mv4wd); see licensing terms below.

# Resources

Build instructions from the original project are copied in [wiki/](wiki/Home.md) ([mv4wd wiki](https://github.com/mv4wd/RCHourglass/wiki/)): decoder, transponder, protocol, compatibility.

The main community thread, with build reports and a lot of practical info, is [RCHourglass DIY Lap Timing (AKA Cano revised)](https://www.rctech.net/forum/radio-electronics/1002584-rchourglass-diy-lap-timing-aka-cano-revised.html) on RCTech. Example: [page 15](https://www.rctech.net/forum/radio-electronics/1002584-rchourglass-diy-lap-timing-aka-cano-revised-15.html).

# How to contribute
Right now the most useful contribute would be feedback in the system performance/build reports/electronic design (for example PCBs).

# Licensing terms
Short version: if you build it for your personal use, you're only kindly requested to donate a small sum to a children
charity of your choice (use 'RC Hourglass for children' as a reference).

Please feedback your donations to:charity dot rchourglass at gmail.com

Please consider donating 5 euros per transponder and 30 euros for the decoder for personal use. 
If the transponder is used in a club/circuit with an admission fee, please consider dontaing 100 euros for the decoder.

The original RCTech thread author/designer (Howard Cano) license applies to the decoder project:

*"All information presented on this thread is free for use for personal, non-commercial purposes.
Contact me for licensing arrangements if you wish to produce and market the decoder."* -user howardcano on rctech

Additional licensing terms for the PSOC firmware/design & transponder by mv4wd:

"All information shared is free for use for personal, non-commercial purposes. 
Contact me for licensing arrangements if you wish to produce and market the decoder.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

Any derivative work source code/design must be public and use this licensing terms. 

Any device derived from this project must respond to the command 'License' with this text.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANYKIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OROTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE." Marco Venturini - mv4wd


