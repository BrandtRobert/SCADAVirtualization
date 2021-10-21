## SCADA Simulator Used For Colorado State University

This SCADA simulator is intended for the use and study of natural 
gas pipelines and other critical infrastructure SCADA systems. The ultimate goal of
this work is to make the world a safer place by allowing us to study the impact of 
cyberattack in a safe and reproducable environment. For description of this work you can
read the thesis dissertation 'Applications of Simulation in SCADA and ICS Security' which
will soon be published on CSU's online repository.

### Installation and Running Simulations

The attached document 'Simulink Installation and Running Simulations' will give you the
necessary descriptions required for downloading and installing MATLAB, and setting up the software
for simulation. We hope to publish more documentation as we continue to finalize the first
stages of the project.

### Python Packages

#### Model

The model package contains source code for the simulink interface (described in detail in the thesis 
dissertation), the source for virtual plcs, in house modbus communication software, as well as
the necessary matlab and simulink files for running the physical simulations. The bulk
of our work is contained in this package, as these components contain most of the modelling 
for both physical system modeling and virtual / simulated PLCs.

#### Controller

The controller package contains source code for our "false actors" which are system operators
modelled with simple matlab scripts. The critical components of this portion of the system are
the sensorbus, the datacollector and a series of basic scripts for interacting with the virtual
controllers. If you are building your own simulations and would like to write code to interact
with the virtual PLCs through modbus reading through this source is good place to start.

#### Devices

This package is still in development. It will contain the interface required for physical devices 
to communicate with the simulator.

#### Frontend / SCADA 

This package is still in development. Its primary objective is to create a graphical interface
for interacting with simulations as they run. Being able to create and interact using control panels
can be a very visceral way to interact with simulations. However, most of our simulation work
does not yet run in discrete real time, meaning that the GUI will have less of an interactive effect.
