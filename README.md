# Real-time Motion Capture Feedback
Completed:
* Streaming marker data via Python Nexus SDK
* Computing foot progression angle in the direction of gait progression
* Triggering haptic cue to the GaitGuide via Bluetooth
* Integrate step-detection script into feedback loop
* Add error catching for when a marker is occluded
* Combine haptic triggers with feedback loop
* Craft baseline FPA estimation script
* Set naming and saving conventions, folder structure
* Test feedback scaling slope
* Pilot test vibrotactile sensitivity ML App
* Write Python script for Vicon for proprioceptive sensitivity test
* Pilot test proprioceptive sensitivity

To do:
* get metronome app
* add timeout for toe-in trial (5 min)
* add catch trials at set number of steps
* add timestamp for when we started feedback 
* set subject numbering, file structure, saving protocol
* proprio code: add coordinates for reference angles for proprio, fix marker labeling, add pseudorandom presentation, add ankle marker
* Quantify delay/estimate how long it takes to detect a step and send a command
* Run pilot trial start to finish
