function [loadParm,lastLoadChange] = gasLoadParameters(conf)
% sets the load profiles for all of the gas loads on the system.  

    %% Some standard factors; can be modified
    cutOutPressureRatio=0.5;
    rampTime=600;
    
    %% define the loads
    loadParm=table();
    
    %% Big Plants
    pNom=600;
    pCut=pNom*cutOutPressureRatio;
    pwr=[0 5];
    pwr=[pwr; add_ramp(3600*12,rampTime,15,30)];
    pwr=[pwr; add_ramp(3600*30,rampTime,30,45)];
    pwr=[pwr; add_ramp(3600*24*3,rampTime,45,60)];
    pwr=[pwr; add_ramp(3600*24*4,rampTime,60,45)];
    pwr=[pwr; add_ramp(3600*24*5,rampTime,45,15)];
    loadParm=[loadParm; add_load("PP Cherokee 1",pwr,pNom,pCut)];
    
    % small plant in center of main line
    pwr=[0 5];
    pwr=[pwr; add_ramp(3600*24*1.5,rampTime,5,10)];
    pwr=[pwr; add_ramp(3600*24*2.2,rampTime,10,12)];
    pwr=[pwr; add_ramp(3600*24*3.7,rampTime,12,8)];
    pwr=[pwr; add_ramp(3600*24*4.1,rampTime,8,5)];
    loadParm=[loadParm; add_load("PP Watkins 1",pwr,pNom,pCut)];
 
    % cyclic gas load on parallel line
    time=1:3:24*10;     % a few days of data a few hours at a time
    l1=cos(time/24*2*pi)'+2;
    pwr=[time(:)*3600 l1(:)];
    loadParm=[loadParm; add_load("DS Denver 1",pwr,pNom,pCut)];
    
    %% Constant load on a regulated lower pressure line
    % small plant in center of main line
    pNom=300;
    pCut=pNom*cutOutPressureRatio;
    smallLoad=0.2;
    pwr=[0 smallLoad];
    pwr=[pwr; add_ramp(3600*24*1.5,rampTime,smallLoad,smallLoad*2)];
    pwr=[pwr; add_ramp(3600*24*2.3,rampTime,smallLoad*2,smallLoad)];
    pwr=[pwr; add_ramp(3600*24*4.5,rampTime,smallLoad,smallLoad*2)];
    loadParm=[loadParm; add_load("DS Small",pwr,pNom,pCut)];
    
    % adding aux load
    pNom=600;
    pCut=pNom*cutOutPressureRatio;
    pwr=[0 5];
    pwr=[pwr; add_ramp(3600*12,rampTime,5,10)];
    pwr=[pwr; add_ramp(3600*30,rampTime,10,15)];
    pwr=[pwr; add_ramp(3600*24*3,rampTime,15,10)];
    pwr=[pwr; add_ramp(3600*24*4,rampTime,10,5)];
    pwr=[pwr; add_ramp(3600*24*5,rampTime, 5,2)];
    loadParm=[loadParm; add_load("PP Aux 1",pwr,pNom,pCut)];
 


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

