function [dx] = gasSetEndingTime(dx,stopTime)
    % sets the end of a time series to the ending time requested by the overall
    % simulation.
    
    dx=dx(dx(:,1)<stopTime,:);       % trim data to fit in time series
    dx=[dx; stopTime dx(end,2:end)];
end

