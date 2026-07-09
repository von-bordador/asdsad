#AI Prompt Ledger

Student ID: 20241000
Repository: asdasd

## Bug 1: Buffer Leak / Encapsulation Flaw

### Exact engineering prompt fed to the AI
How do I fix a Python mutable default argument bug in a TelemetryBuffer class where frame_buffer=[] causes multiple sensor buffers to share the same list?

### Why the AI's initial suggestion failed in an embedded hardware context
A simple shared-list fix may ignore that each hardware channel must keep an isolated telemetry queue. In an avionics-style bus, shared buffers can mix LiDAR, GPS, and IMU packets, making diagnostics unreliable.

### Computer engineering justification for the final implemented code
The constructor should use frame_buffer=None and allocate a new list for each TelemetryBuffer instance. This preserves encapsulation because each peripheral owns its own independent frame buffer.

## Bug 2: Polymorphic Trap / LSP Violation

### Exact engineering prompt fed to the AI
How do I fix an LSP violation where IMUPeripheral.poll_raw_voltage sometimes returns a dictionary error packet instead of a float voltage, causing normalization math to fail?

### Why the AI's initial suggestion failed in an embedded hardware context
Returning mixed data types from hardware polling breaks the bus controller pipeline. The controller expects all peripherals to return numeric voltage readings, so returning a dictionary can crash signal normalization.

### Computer engineering justification for the final implemented code
IMUPeripheral.poll_raw_voltage should always return a float. If drift is detected, the code can log a warning or push a safe fault value, but the method must still return numeric voltage data so downstream processing remains stable.

## Bug 3: Race Condition / Concurrency Flaw

### Exact engineering prompt fed to the AI
How do I fix a race condition in a Python threaded AvionicsBusMaster where multiple worker threads update active_bus_register and total_cycles_executed at the same time?

### Why the AI's initial suggestion failed in an embedded hardware context
Only reducing thread delay or changing timing does not solve the real concurrency issue. In embedded bus control, shared register updates must be atomic because timing-dependent fixes can fail under different CPU loads.

### Computer engineering justification for the final implemented code
A threading.Lock should protect the critical section where shared bus registers and cycle counters are updated. This ensures only one worker thread modifies shared telemetry state at a time.
