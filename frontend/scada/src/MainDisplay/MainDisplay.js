import {CardColumns} from "react-bootstrap";
import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import PLC from "./PLC.js";


export default class MainDisplay extends React.Component {
    constructor(props){
        super(props)
        this.list = new Array(10)
        for (let i = 1; i < 7; i++){
            this.list.push(i)
        }
        this.columnStyle = {
            columnCount: 2,
        }
    }
    render(){
        return (
            <div>
                <CardColumns style={this.columnStyle}>
                    {this.list.map((number) => <PLC 
                                                PLCID={number} 
                                                gaugeID={"gauge"+number}
                                                key={"gauge" + number}
                                                />)}
                </CardColumns>
            </div>

        )
    }
}