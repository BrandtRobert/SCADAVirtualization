function [valveParm] = gasValveParameters(conf)
% creates control instructions for all valves in the system
    
    tRamp=60;       % time to open or close the valve
    
    valveParm=table();
    
    %% Set one
    dx=[0 true];
    dx=[dx; add_transition(dx,3600*24*2.1)];
    dx=[dx; add_transition(dx,3600*24*3.2)];
    dx=[dx; add_transition(dx,3600*24*3.8)];
    dx=[dx; add_transition(dx,3600*24*4.1)];
    valveParm=[valveParm;add_valve("Cherokee 2 Valve",dx,20)];
    
    % Stub line to Watkins to test shutoff
    dx=[0 true];
    dx=[dx; add_transition(dx,3600*24*1.9)];
    dx=[dx; add_transition(dx,3600*24*2.2)];
    valveParm=[valveParm;add_valve("Watkins Stub Valve",dx,20)];
    
    dx = [0 true];
    valveParm=[valveParm;add_valve("Watkins Stub Valve Ext",dx,20)];
    
    %% Defines one gas load
    function tx=add_valve(name,timeData,diameterInches)
        timeData=gasSetEndingTime(timeData,conf.StopTime);
        tx=table();
        tx.Name=name;
        tx.Time={timeData(:,1)}; 
        tx.State={timeData(:,2)};
        tx.PortDiameter=diameterInches;         % diameter of pipe 
        tx.MaxValveDiameter=diameterInches-1;   % maximum clearance through the valve
    end

    %% Create one step in the load profile
    function data=add_transition(data,atTime)
        data=[
            atTime          data(end,2);
            atTime+tRamp    not(data(end,2));
            ];
    end
end

