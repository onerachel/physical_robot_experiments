# Running Physical Robot Experiments in Dynamic Environments
The two physical robots used in these experiments are the best-performing models from the Lamarckian and Darwinian systems, as determined in the simulator. The results can be found at https://github.com/onerachel/Lamarckism_Environments

Parameters used in the experiments are:
``` 
ENVIRONMENT = "FLAT" or "RUGGED" # type of environment
ROBOT_TYPE = "Lamarckian_Evolved_Robot" or "Darwinian_Evolved_Robot"

``` 

## Prerequisites
```
1. Raspberry Pi 3
2. Raspberry Pi HAT (for extending the camera sensor etc)
3. Raspberry Pi Camera
4. SSD Card
```

```
Limitations of the Hardware:
Reason for Using These Servo Motors: We use these particular servo motors, which lack feedback, because the Raspberry Pi HAT in our setup only has three pins per servo, instead of four. The additional pin would typically be used for feedback.
Reason for Using This Older Raspberry Pi HAT: We opted for this older model of the Raspberry Pi HAT because the newer version includes a security switch that causes an immediate shutdown when higher voltages are detected, which can occur with many active hinges.
Future Work: We plan to redesign the Raspberry Pi HAT to support higher voltage servos, include battery usage compatibility, and add extra pin lines for servo feedback.
```

## Installation 

Step 1 

(You can skip this step and directly use the 'brains_pickle' file we have generated.)

```
1. git clone https://github.com/onerachel/Lamarckism_Environments.git
2. cd Lamarckism_Environments
3. virtualenv -p=python3.8 .venv
4. source .venv/bin/activate
5. ./dev_requirements.sh
6. python lamarckian_evolution/rerun_best_lamarckism.py
7. python darwinian_evolution/rerun_best_darwinism.py 
create and save lamarc_brain.pickle and darw_brain.pickle
``` 

Step 2 

On a SSD card, install:

```
git clone https://github.com/onerachel/physical_robot_experiments.git

[note: This is not the default revolve2 version, make sure to install modular_robot and modular_robot_physical packages with the updated ( _brain_cpg_instance_environmental_control.py & _brain_cpg_network_static_environmental_control and _brain_cpg_network_static) under modular_robot/brain/cpg]
```

Step 3 

Copy config.ipynb notebook to Raspberry Pi (all the pickle files used in this notebook are also there):

```
scp <config.ipynb> pi@<ip>:~/.

```

Step 4

For recording the experiments and calculate the fitness etc, additional recording camera is setup:

```
python run_recording_cameras.py

```

## Run experiments 
To run experiments

``` 
python run_experiment.py
``` 

