from labjack import ljm
import time

labjack = ljm.openS("T7", "USB", "ANY")

#Link the script to a specific Lua script file
luaScript = ("LJ.IntervalConfig(0, 500)\n"
    "while true do\n"
    "    if LJ.CheckInterval(0) then\n"
    "        print(LJ.Tick())\n"
    "    end\n"
    "end\n")

scriptLength = len(luaScript)

ljm.eWriteName(labjack, "LUA_RUN", 0)
time.sleep(0.6)
ljm.eWriteName(labjack, "LUA_RUN", 0)

ljm.eWriteName(labjack, "LUA_SOURCE_SIZE", scriptLength)
ljm.eWriteNameByteArray(labjack, "LUA_SOURCE_WRITE", scriptLength, luaScript)

ljm.eWriteName(labjack, "LUA_DEBUG_ENABLE", 1)
ljm.eWriteName(labjack, "LUA_DEBUG_ENABLE_DEFAULT", 1)
ljm.eWriteName(labjack, "LUA_RUN", 1)

ljm.closeAll()

#C code to manually load a Lua script:
'''
const char * luaScript =
    "LJ.IntervalConfig(0, 500)\n"
    "while true do\n"
    "  if LJ.CheckInterval(0) then\n"
    "    print(LJ.Tick())\n"
    "  end\n"
    "end\n"
    "\0";

const unsigned scriptLength = strlen(luaScript) + 1;
// strlen does not include the null-terminating character, so we add 1
// byte to include it.

int handle = OpenOrDie(LJM_dtT7, LJM_ctANY, "LJM_idANY");

// Disable a running script by writing 0 to LUA_RUN twice
WriteNameOrDie(handle, "LUA_RUN", 0);
// Wait for the Lua VM to shut down (and some T7 firmware versions need
// a longer time to shut down than others):
MillisecondSleep(600);
WriteNameOrDie(handle, "LUA_RUN", 0);

// Write the size and the Lua Script to the device
WriteNameOrDie(handle, "LUA_SOURCE_SIZE", scriptLength);
WriteNameByteArrayOrDie(handle, "LUA_SOURCE_WRITE", scriptLength, luaScript);

// Start the script with debug output enabled
WriteNameOrDie(handle, "LUA_DEBUG_ENABLE", 1);
WriteNameOrDie(handle, "LUA_DEBUG_ENABLE_DEFAULT", 1);
WriteNameOrDie(handle, "LUA_RUN", 1);
'''