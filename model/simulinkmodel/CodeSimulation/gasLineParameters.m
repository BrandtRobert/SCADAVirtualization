function [lineParm,pNom] = gasLineParameters(conf)
    % Creates the line parameters for the all line segments in the simulation,
    % including valves and other equipment
    
    %% Nominal starting pressure
    pNom=600;       % psia
    %% Transmission lines
    lineParm=table();
%     lineParm=[lineParm;add_line("Main 1",24,50,pNom)];
    lineParm=[lineParm;add_line("Main 1",48,50,pNom)];
    lineParm=[lineParm;add_line("Main 2",24,35,pNom)];
    lineParm=[lineParm;add_line("Parallel 1",20,17,pNom)];
    lineParm=[lineParm;add_line("Parallel 2",20,72,pNom)];
    lineParm=[lineParm;add_line("Watkins Stub",20,4,pNom)];
    
    %% Transmission line stubs
    lineParm=[lineParm;add_line("Stub 1",10,8,pNom/2)];
   
    % aux line
    lineParm=[lineParm;add_line("Aux 1",24,50,pNom)];
    
    %% Defines one segment of line; add parameters for more complex line designs
    function tx=add_line(name,diameter,length,nominalPressure)
        tx=table(name,diameter,length,nominalPressure ...
            ,'VariableNames',{'Name' 'DiameterInch' 'LengthMiles' 'StartPressurePSI'} ...
            );   
    end
end

