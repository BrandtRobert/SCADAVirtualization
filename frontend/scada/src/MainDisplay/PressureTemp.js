import React from "react";
import {Col, Row} from "react-bootstrap";
import GaugeChart from "react-gauge-chart";
import Thermometer from "react-thermometer-component";
import Bulb from "react-bulb";
import './plc.css';

export default class PressureTemp extends React.Component {
    constructor(props) {
        super(props)

        this.createPressureAndTemp = this.createPressureAndTemp.bind(this)
        const tempStats = this.createPressureAndTemp();

        this.state = {
            chartStyle: {
                height: 30
            },
            stats: tempStats
        }
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => this.update(),
            1000
          );
    }

    update() {
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

        this.setState({ stats: tempStats});
    }

    createPressureAndTemp() {
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

    createGauges() {
        const chartStyle = {
            height: 100,
            width: 230
        }
        return <Row bsPrefix="gauges">
                        <Col bsPrefix="pressure">
                            <Row bsPrefix="pressureRow">
                                <GaugeChart 
                                    nrOfLevels={3} 
                                    colors={["#FF5F6D", "#00ff7f", "#FF5F6D"]}
                                    textColor={"#00ff7f"}
                                    percent={this.state.stats.pressure} 
                                    id={this.props.gaugeID} 
                                    style={chartStyle}
                                    formatTextValue={(value) => {return ((value / 100) * 1200).toFixed(2) + " psi"} }
                                />
                            </Row>
                            <Row bsPrefix="indicator">
                                <Bulb
                                    size={10}
                                    color={ this.state.stats.pressureInd }
                                />
                            </Row>
                            <Row bsPrefix="errorTag">
                                WARNING
                            </Row>
                        </Col>
                        <Col bsPrefix="temp">
                            <Row bsPrefix="thermo">
                                <Thermometer
                                    max={250}
                                    format={" F°"}
                                    theme={"dark"} 
                                    size={"normal"} 
                                    height="140" 
                                    value={this.state.stats.temp}
                                />
                            </Row>
                            <Row bsPrefix="indicator">
                                <Bulb
                                    size={10}
                                    color={ this.state.stats.tempInd }
                                />
                            </Row>
                            <Row bsPrefix="errorTag">
                                WARNING
                            </Row>
                        </Col>  
                </Row>;
    }

    render() {
        return (
            <Col bsPrefix="TEST">
                { this.createGauges() }
            </Col>   
        )

    }
}
