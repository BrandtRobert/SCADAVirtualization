function [lineParm,pNom] = gasLineParameters(conf, systemPressure)
    % Creates the line parameters for the all line segments in the simulation,
    % including valves and other equipment
    
    %% Nominal starting pressure
    pNom=systemPressure;       % psia
    %% Transmission lines
    lineParm=table();
    
    % 1
    lineParm=[lineParm;add_line("Cheyenne to Fort Collins",32,45,pNom)];
    % 2
    lineParm=[lineParm;add_line("Fort Collins to Longmont",32,40,pNom)];
    % 3
    lineParm=[lineParm;add_line("Longmont to Denver",32,40,pNom)];
    % 4
    lineParm=[lineParm;add_line("Denver to Colorado Springs",16,70,pNom)];
    % 5
    lineParm=[lineParm;add_line("Colorado Springs to Trindad",16,130,pNom)];
    % 6
    lineParm=[lineParm;add_line("Longmont to Cheyenne Wells",16,200,pNom)];
    % 7
    lineParm=[lineParm;add_line("Cheyenne Wells to Springfield",16,130,pNom)];
    %8
    lineParm=[lineParm;add_line("Cheyenne to Fort Morgan",16,100,pNom)];
    %9
    lineParm=[lineParm;add_line("Fort Morgan to Longmont",16,105,pNom)];
    %10
    lineParm=[lineParm;add_line("Fort Morgan to Denver",16,200,pNom)];
    %11
    lineParm=[lineParm;add_line("Cheyenne Wells to CO Springs",16,71,pNom)];
    %12
    lineParm=[lineParm;add_line("CO Springs to Springfield",16,125,pNom)];
    
    %% Defines one segment of line; add parameters for more complex line designs
    function tx=add_line(name,diameter,length,nominalPressure)
        tx=table(name,diameter,length,nominalPressure ...
            ,'VariableNames',{'Name' 'DiameterInch' 'LengthMiles' 'StartPressurePSI'} ...
            );   
    end
end

