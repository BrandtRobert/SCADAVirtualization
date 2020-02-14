function [conf] = gasConfig()
    % create a configuration structure for the simulation
    
    % Simulation timing
    conf.StopTime=7*24*3600;        % in seconds
    conf.StableTime=4*24*3600;    % in seconds

    % distribution feed lines
    conf.DistributionPressure=300;  % psia
    
    % short hand for fuel consumption
    efficiency=0.33;    % typical simple cycle efficiency
    hhvGas=46544;       % heating value of typical NG, kJ/kg
    inputPerKJ=1/efficiency;    % input watts per output watts
    kgPerKJ=inputPerKJ/hhvGas;  % gas required per unit output energy, kg/kJ
    conf.kgPerSecondPerKW=kgPerKJ;  % on a per second basis, kJ/s=kW
    
    % Conversions
    conf.MPaToPSI=145.038;
    conf.gPerSCF=19.2;          % grams per standard cubic foot @ 60F/1 atm
    conf.kgToSCF=1000/conf.gPerSCF; % kg/scf
end
