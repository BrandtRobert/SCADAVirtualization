%% Initalize the workspace
path(path,'CodeSimulation'); 
path(path,'CodeOutput'); 

% modelName="c_station_v2";
modelName="c_station_v3";

%% Load model and grab its handle
hModel=load_system(modelName);

%% Create configuration
conf=gasConfig();
[lineParm,conf.UpstreamPressure]=gasLineParameters(conf);
[loadParm,lastLoadChange]=gasLoadParameters(conf);
[valveParm]=gasValveParameters(conf);

%% Create stable starting point conditions - Step 1, all loads off
% switch off all loads, and simulate
set_param(hModel,'SimscapeUseOperatingPoints','off');
loadControlFlag="off";
valveControlFlag="initial";
set_param(modelName,'StopTime',string(conf.StableTime));    % set time to stable with no loads
sim(modelName);                                     % simulate
op=simscape.op.create(simlog,conf.StableTime);      % capture ending state as initialization state
set_param(hModel,'SimscapeUseOperatingPoints','on'); % turn on the operating state
drawnow(); % in case the viewer is open

%% Create stable startup conditions - Step 2, ramp loads to initial values
loadControlFlag="initial";
valveControlFlag="initial";
sim(modelName);                                     % simulate
op=simscape.op.create(simlog,conf.StableTime);      % capture ending state as initialization state

% finally set stop time to handle entire simulation
loadControlFlag="on";
valveControlFlag="on";
set_param(modelName,'StopTime',string(conf.StopTime));    % set time to stable with no loads
