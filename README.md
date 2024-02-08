# Real-time Motion Capture Feedback
Completed:
* Streaming marker data via Python Nexus SDK
* Computing foot progression angle in the direction of gait progression
* Triggering haptic cue to the GaitGuide via Bluetooth
* Integrate step-detection script into feedback loop
* Add error catching for when a marker is occluded

To do:
* Combine haptic triggers with feedback loop
  * Decide whether asyncio is right to use here?
* Quantify delay/estimate how long it takes to send a command
