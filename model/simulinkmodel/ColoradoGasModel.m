%% Initalize the workspace
path(path,'ColoradoGasModel'); 
path(path,'CodeOutput'); 

% modelName="c_station_v2";
modelName="coloradoGasModel";
stableTime=4*24*3600;
% 3 day run time
stopTime=5*24*3600;
systemPressure=800;
shutOffPoint=600;
shutOffDuration=3600;

%% Load model and grab its handle
hModel=load_system(modelName);

%% Create configuration
conf=gasConfig();
[lineParm,conf.UpstreamPressure]=gasLineParameters(systemPressure);
[loadParm,lastLoadChange,plantCapacities]=gasLoadParameters(conf, systemPressure);
% [valveParm]=gasValveParameters(conf);
maxCapacity=sum(plantCapacities);
shutOffDuration=3600;
shutOffPoint=600;

systemLoad=loadParm(1,:);

%% Create stable starting point conditions - Step 1, all loads off
% switch off all loads, and simulate
set_param(hModel,'SimscapeUseOperatingPoints','off');
loadState="off";
% valveControlFlag="initial";
set_param(modelName,'StopTime',string(conf.StableTime));    % set time to stable with no loads
s=sim(modelName);                                     % simulate
op=simscape.op.create(s.simlog,stableTime);     % capture ending state as initialization state
set_param(hModel,'SimscapeUseOperatingPoints','on'); % turn on the operating state
drawnow(); % in case the viewer is open

%% Create stable startup conditions - Step 2, ramp loads to initial values
loadState="initial";
% valveControlFlag="initial";
s = sim(modelName);                                     % simulate
op=simscape.op.create(s.simlog,stableTime);      % capture ending state as initialization state

% finally set stop time to handle entire simulation
loadState="on";
valveControlFlag="on";
set_param(modelName,'StopTime',string(stopTime));    % set time to stable with no loads

