import React from "react";
import {Col, Row} from "react-bootstrap";
import GaugeChart from "react-gauge-chart";
import Thermometer from "react-thermometer-component";
import Bulb from "react-bulb";

export default class miniSim {
    generatePressureAndTemp() {
        const tempStats = {
            pressure: 0,
            temp: 0,
            pressureInd: "",
            tempInd: ""
        };
        
        const pressure = Math.floor(Math.random() * (1200 - 600) + 600);
        //console.log(pressure);
        tempStats.pressure = pressure / 1200;
        //console.log(tempStats.pressure);
        tempStats.temp = Math.floor(Math.random() * (200 - 100) + 100);
        console.log(tempStats.temp);
        if (tempStats.pressure > 0.66 || tempStats.pressure < 0.33){
            tempStats.pressureInd = "red";
        } else {
            tempStats.pressureInd = "black";
        }
        if (tempStats.temp > 50){
            tempStats.tempInd = "red";
        } else {
            tempStats.tempInd = "black";
        }
        return tempStats;
    }

    updateData() {
        const tempStats = this.state.stats;
        const test = Math.random();
        if (test > 0.5){
            let tempPressure = tempStats.pressure * 1200;
            tempPressure += test + 50;
            if (tempPressure > 1200){ tempPressure = 1200;}
            tempStats.pressure = tempPressure / 1200;
            
            let tempTemp = tempStats.temp;
            tempTemp += Math.floor(test + 1);
            if (tempTemp > 250) { tempTemp = 250; }
            tempStats.temp = tempTemp;
        } else {
            let tempPressure = tempStats.pressure * 1200;
            tempPressure -= test + 50;
            if (tempPressure < 0){ tempPressure = 0;}
            tempStats.pressure = tempPressure / 1200;

            let tempTemp = tempStats.temp;
            tempTemp -= Math.floor(test + 1);
            if (tempTemp < 0) { tempTemp = 0; }
            tempStats.temp = tempTemp;
        }

        if (tempStats.pressure > 0.66 || tempStats.pressure < 0.33){
            tempStats.pressureInd = "red";
        } else {
            tempStats.pressureInd = "black";
        }
        if (tempStats.temp > 200){
            tempStats.tempInd = "red";
        } else {
            tempStats.tempInd = "black";
        }
        return tempStats;
    }
}