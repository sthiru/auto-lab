# LabVIEW Implementation Guide for Micromotion Controller

## Overview
This guide provides detailed instructions for implementing the LabVIEW module to control a 1-axis linear stage using the micromotion controller protocol.

## Hardware Requirements
- Linear stage with micromotion controller
- Serial communication cable
- Computer with LabVIEW (2019 or later)
- VISA drivers for serial communication

## Software Components

### 1. Main VI: Micromotion_Controller_LabVIEW.vi
**Front Panel Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│                     CONNECTION PANEL                        │
│ COM Port: [COM8________]  [Connect]  [Disconnect]          │
│ Status: [● Ready] [○ Connected] [○ Error]                  │
├─────────────────────────────────────────────────────────────┤
│                     MOVEMENT CONTROL                        │
│ Position (steps): [0________]                              │
│ Direction: ○ Positive ○ Negative                           │
│ Acceleration: [0___] Deceleration: [0___]                   │
│ [MOVE] [STOP] [HOME]                                        │
├─────────────────────────────────────────────────────────────┤
│                     SPEED CONTROL                           │
│ Speed (5-4000): [1000____] [SET SPEED]                     │
├─────────────────────────────────────────────────────────────┤
│                     STATUS DISPLAY                          │
│ Current Position: [0________]                              │
│ Movement Status: [Idle___________]                         │
│ Limit Switch: [None____________]                          │
│ Error Message: [________________]                          │
└─────────────────────────────────────────────────────────────┘
```

### 2. Block Diagram Implementation

#### Serial Communication Setup
```labview
VISA Configure Serial Port
├── VISA Resource Name: COM Port control
├── Baud Rate: 19200
├── Data Bits: 8
├── Parity: 0 (None)
├── Stop Bits: 1
└── Flow Control: 0 (None)
```

#### Controller Initialization Sequence
```labview
Case Structure: Connect Button Pressed
├── True Case:
│   ├── VISA Configure Serial Port
│   ├── Wait (100 ms)
│   ├── VISA Write: [100]
│   ├── Wait (100 ms)
│   ├── VISA Read
│   ├── Compare to [200]
│   ├── Set Connection Status LED
│   └── Error Handler
└── False Case: Do nothing
```

#### Movement Control Implementation
```labview
Case Structure: Move Button Pressed
├── True Case:
│   ├── Send [19] (Initiate Movement)
│   ├── Calculate XByte Sequence (Sub VI)
│   ├── Send XByte2, XByte1, XByte0 sequentially
│   ├── Send Direction Byte
│   ├── Send Acceleration Byte
│   ├── Send Deceleration Byte
│   ├── Check ACK [10]
│   ├── Monitor Status (40=Home, 41=Far)
│   ├── Send [163] (Complete Movement)
│   └── Send [10][10][10] (Finalize)
└── False Case: Do nothing
```

### 3. Sub VIs

#### Calculate_XByte_Sequence.vi
**Inputs:** Position (I32)
**Outputs:** XByte2, XByte1, XByte0 (U8 arrays)

**Implementation:**
```labview
Position → Format Value (Hexadecimal, 6 digits) → 
String Subset → Hex to Number → Build Array
```

#### Send_Command_With_ACK.vi
**Inputs:** Command Byte, Expected ACK
**Outputs:** Success Boolean, Error Message

**Implementation:**
```labview
VISA Write Command → Wait (100ms) → VISA Read → 
Compare to Expected ACK → Boolean Output
```

#### Check_Controller_Status.vi
**Inputs:** VISA Reference
**Outputs:** Status String, Limit Status

**Implementation:**
```labview
VISA Read → Case Structure:
├── 40 → "Home limit reached"
├── 41 → "Far limit reached"
├── 170 → "Movement completed"
└── Default → "Unknown status"
```

## Protocol Implementation Details

### Command Codes
| Function | Command | Expected Response |
|----------|---------|------------------|
| Initialize | 100 | 200 |
| Move Initiate | 19 | 10 |
| Speed Set | 34 | 10 |
| Movement Complete | 163 | - |
| Stop | 104 | - |
| Finalize | 10 | - |

### Data Conversion
- **Position:** Decimal → 6-digit hex → 3 bytes (MSB to LSB)
- **Speed:** Decimal → 4-digit hex → 2 bytes (MSB to LSB)
- **Direction:** Positive=125, Negative=175

### Timing Requirements
- Wait 100ms between each command
- Serial timeout: 1000ms
- Movement completion: Monitor status byte

## Error Handling

### Communication Errors
- VISA timeout handling
- Invalid response codes
- Serial port connection issues

### Motion Errors
- Limit switch detection
- Invalid position values
- Speed out of range (5-4000)

### Implementation
```labview
Error Cluster → Case Structure:
├── No Error → Continue execution
└── Error → Display message, stop operation
```

## Usage Instructions

### 1. Initial Setup
1. Connect the linear stage to the computer via serial cable
2. Open LabVIEW and load Micromotion_Controller_LabVIEW.vi
3. Set the correct COM port number
4. Click "Connect" to establish communication

### 2. Basic Movement
1. Enter desired position in steps
2. Select direction (Positive or Negative)
3. Set acceleration and deceleration if needed
4. Click "MOVE" to execute movement

### 3. Speed Control
1. Enter speed value (5-4000)
2. Click "SET SPEED"
3. Verify speed setting success

### 4. Safety Features
- "STOP" button immediately halts movement
- "HOME" button returns to home position
- Limit switch status monitoring
- Error message display

## Testing Procedure

### 1. Communication Test
- Verify connection status LED turns green
- Check for "Controller ready" message

### 2. Movement Test
- Test small movements (±100 steps)
- Verify position updates
- Check limit switch detection

### 3. Speed Test
- Test various speed settings
- Verify speed range compliance

## Troubleshooting

### Common Issues
1. **Connection Failed**
   - Check COM port number
   - Verify cable connection
   - Ensure controller power

2. **Movement Not Responding**
   - Check position value format
   - Verify direction setting
   - Check for limit switch activation

3. **Speed Setting Failed**
   - Verify speed range (5-4000)
   - Check communication status
   - Retry speed setting

### Debug Mode
Enable front panel debugging to monitor:
- Serial communication bytes
- Response codes
- Timing between commands
- Error clusters

## Integration with Other Systems

### DLL Export
The VI can be compiled into a DLL for use with:
- C/C++ applications
- Python (using ctypes)
- MATLAB
- TestStand

### Network Distribution
Use LabVIEW Web Services to:
- Control stage remotely
- Monitor status via web interface
- Integrate with SCADA systems

## Performance Considerations

### Optimization Tips
- Use VISA events for asynchronous communication
- Implement buffered reading for status monitoring
- Use state machine for complex motion sequences

### Real-time Requirements
- For high-speed applications, consider LabVIEW Real-Time
- Use deterministic timing for precise positioning
- Implement hardware-timed I/O if available
