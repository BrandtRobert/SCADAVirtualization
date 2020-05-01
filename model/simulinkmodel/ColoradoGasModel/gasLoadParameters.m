function [loadParm,lastLoadChange,loadCapacities] = gasLoadParameters(conf, systemPressure)
% sets the load profiles for all of the gas loads on the system.  

    %% Some standard factors; can be modified
    cutOutPressureRatio=0.5;
    rampTime=600;
    
    %% define the loads
    loadParm=table();
    
    %% Big Plants
    pNom=systemPressure;
    pCut=pNom*cutOutPressureRatio;
    pwr=[0 5];
    loadCapacities=[];
    
    pwr=[pwr; add_ramp(3600*12,rampTime,5,120)];
    % Large ramp within the system
    % from about .1 to almost max capacity in an hour
    % Denmark ~ 2000 20% wind displacement, peak power was 80%
    pwr=[pwr; add_ramp(3600*30,3600,120,400)];
    pwr=[pwr; add_ramp(3600*24*3,rampTime,400,425)];
    pwr=[pwr; add_ramp(3600*24*4,rampTime,425,225)];
    pwr=[pwr; add_ramp(3600*24*5,rampTime,225,250)];
    loadParm=[loadParm; add_load("System Load",pwr,pNom,pCut)];
    
    % not in use because of system load (2)
    pwr=[0 5];
    pwr=[pwr; add_ramp(3600*12,rampTime,15,30)];
    pwr=[pwr; add_ramp(3600*30,rampTime,30,45)];
    pwr=[pwr; add_ramp(3600*24*3,rampTime,45,60)];
    pwr=[pwr; add_ramp(3600*24*4,rampTime,60,45)];
    pwr=[pwr; add_ramp(3600*24*5,rampTime,45,15)];
    loadParm=[loadParm; add_load("PP Fort Collins",pwr,pNom,pCut)];
    loadCapacities=[loadCapacities,75];
    
    % PP Denver (3)
    pwr=[0 5];
    pwr=[pwr; add_ramp(3600*24*1.5,rampTime,5,10)];
    pwr=[pwr; add_ramp(3600*24*2.2,rampTime,10,12)];
    pwr=[pwr; add_ramp(3600*24*3.7,rampTime,12,8)];
    pwr=[pwr; add_ramp(3600*24*4.1,rampTime,8,5)];
    pwr=[pwr; add_ramp(3600*24*4.5,rampTime,8,5)];
    pwr=[pwr; add_ramp(3600*24*5.0,rampTime,8,5)];
    loadParm=[loadParm; add_load("PP Denver",pwr,pNom,pCut)];
    loadCapacities=[loadCapacities,135];
 
    % DS Longmont (4)
    time=1:3:24*10;     % a few days of data a few hours at a time
    l1=cos(time/24*2*pi)'+2;
    pwr=[time(:)*3600 l1(:)];
    loadParm=[loadParm; add_load("DS Longmont",pwr,pNom,pCut)];
    
    % Colorado Springs Power Plant (5)
    pwr=[0 5];
    loadParm=[loadParm; add_load("PP Colorado Springs",pwr,pNom,pCut)];
    loadCapacities=[loadCapacities,75];
    
    % DS Trindad Load (6)
    time=1:3:24*10;     % a few days of data a few hours at a time
    l1=cos(time/24*2*pi)'+2;
    pwr=[time(:)*3600 l1(:)];
    loadParm=[loadParm; add_load("DS Trindad",pwr,pNom,pCut)];
    
    % Colorado Springs Power Plant (7)
    pwr=[0 5];
    loadParm=[loadParm; add_load("PP Cheyenne Wells",pwr,pNom,pCut)];
    loadCapacities=[loadCapacities,75];
    
    % DS Springfield (8)
    time=1:3:24*10;     % a few days of data a few hours at a time
    l1=cos(time/24*2*pi)'+2;
    pwr=[time(:)*3600 l1(:)];
    loadParm=[loadParm; add_load("DS Springfield",pwr,pNom,pCut)];
    
    % Fort Morgan Power Plant (9)
    pwr=[0 5];
    loadParm=[loadParm; add_load("PP Fort Morgan",pwr,pNom,pCut)];
    loadCapacities=[loadCapacities,75];
    
    %% Find the last changing load
    lastLoadChange=0;
    for ix=1:height(loadParm)
        t=loadParm.Time{1};
        lastLoadChange=max([t(end) lastLoadChange]);
    end
    
    %% Defines one gas load
    function tx=add_load(name,timeData,Pnominal,Pcutoff)
        timeData=gasSetEndingTime(timeData,conf.StopTime);
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
end

