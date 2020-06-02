function [] = plotLoadProfile(loadSteps,loadCapacity)
%PLOTLOADPROFILE Summary of this function goes here
%   Detailed explanation goes here
GAS_HEATING_VALUE = 45357;
PLANT_EFF = 0.15;
x = loadSteps.Time;
y = (loadSteps.Data * (GAS_HEATING_VALUE * 1000 * PLANT_EFF)) / 1000000;
plot(x, y)
hold on
x = loadCapacity.Time;
y = (loadCapacity.Data * (GAS_HEATING_VALUE * 1000 * PLANT_EFF)) / 1000000;
plot(x, y)

ylabel('System Wide Power (Megawatts)');
xlabel('Time (in Days)');

xticks(0:86400:345600);
xticklabels(0:1:max(loadCapacity.Time)/86400);

yticks(0:250:3000)

title('Power Generation Over Time');
legend('Required Power Load', 'Current Power Generation');

hold off
end

