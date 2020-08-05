import {Card, Col, Row} from "react-bootstrap";
import React from "react";
import PLC_CONTROLS from "./PLC_Controls.js";
import ConnectionStatus from "./ConnectionStatus.js";
import PressureTemp from "./PressureTemp.js"
import './plc.css';


export default class PLC extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            chartStyle: {
                height: 30
            },
        }

    }


    render() {
        return (
            <Card bg={'secondary'} text={'light'}>
                <Card.Title>
                    PLC {this.props.PLCID}
                    <hr/>
                </Card.Title>
                <Card.Body bsPrefix="plcs">
                    <Row xs={12}>
                        <PressureTemp gaugeID={this.props.gaugeID}/>
                        <Col xs={5}>
                            <PLC_CONTROLS/>
                        </Col>
                    </Row>
                    <Row xs={12}>
                        <ConnectionStatus status={"Connected"}/>
                    </Row>
                </Card.Body>
            </Card>
        )
    }
}