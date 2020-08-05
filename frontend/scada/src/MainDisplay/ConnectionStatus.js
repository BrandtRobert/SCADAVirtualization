import React from "react";
import {Container} from "react-bootstrap";
import './plc.css';

export default class ConnectionStatus extends React.Component{
    render(){
        const className = "connectionStatus" + this.props.status;
        return(
            <div className={className} >
                { this.props.status }
            </div>   
            
        )
    }
}