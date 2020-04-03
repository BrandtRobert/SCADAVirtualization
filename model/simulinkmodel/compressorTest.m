
%% setup model and directory paths
path(path,'CodeSimulation'); 
path(path,'CodeOutput'); 
modelName='CompressorTest';
model=load_system(modelName);

%% start simulation with loads off to reach initial state?
loadState='off';
pNom=600;
rampTime=600;
pCut=pNom*0.5;
stableTime=4*24*3600;
stopTime=7*24*3600;

%% gas load parms
lineParm=[];
lineParm=[lineParm;add_line("Main 1",48,50,pNom)];
lineParm=[lineParm;add_line("Main 2",24,35,pNom)];
lineParm=[lineParm;add_line("Main 3",24,35,pNom)];

% Load 1
loadParm = [];
pwr=[0 5];
pwr=[pwr; add_ramp(3600*12,rampTime,0,25)];
pwr=[pwr; add_ramp(3600*30,rampTime,25,40)];
pwr=[pwr; add_ramp(3600*24*3,rampTime,40,10)];
loadParm=[loadParm; add_load("PP1",pwr,pNom,pCut, stopTime)];

% Load 2
pwr=[0 5];
pwr=[pwr; add_ramp(3600*12,rampTime,0,30)];
pwr=[pwr; add_ramp(3600*30,rampTime,30,40)];
pwr=[pwr; add_ramp(3600*24*3,rampTime,40,20)];
loadParm=[loadParm; add_load("PP2",pwr,pNom,pCut, stopTime)];

% System Load
pwr=[0 0];
pwr=[pwr; add_ramp(3600*12,rampTime,0,30)];
pwr=[pwr; add_ramp(3600*30,rampTime,30,40)];
pwr=[pwr; add_ramp(3600*48,rampTime,40,70)];
pwr=[pwr; add_ramp(3600*24*3,rampTime,70,90)];
systemLoad=add_load("System Load", pwr, pNom, pCut, stopTime);

set_param(model,'SimscapeUseOperatingPoints','off');
set_param(modelName,'StopTime',string(stableTime));
sim(modelName);
op=simscape.op.create(ans.simlog,stableTime);
set_param(model,'SimscapeUseOperatingPoints','on');

loadState='on';
set_param(modelName,'StopTime',string(stopTime));
%% Defines one gas load
function tx=add_load(name,timeData,Pnominal,Pcutoff, stopTime)
    timeData=gasSetEndingTime(timeData,stopTime);
    tx=table();
    tx.Name=name;
    tx.Time={timeData(:,1)}; 
    tx.Load={timeData(:,2)};
    tx.NominalPressure=Pnominal;
    tx.PressureCutoff=Pcutoff;
end

%% Create one step in the load profile
function data=add_ramp(tStart,tRamp,startFlow,endFlow)
    data=[
        tStart          startFlow;
        tStart+tRamp    endFlow;
        ];
end

%% Defines one segment of line; add parameters for more complex line designs
function tx=add_line(name,diameter,length,nominalPressure)
    tx=table(name,diameter,length,nominalPressure ...
        ,'VariableNames',{'Name' 'DiameterInch' 'LengthMiles' 'StartPressurePSI'} ...
        );   
end