import {Container, Row} from "react-bootstrap";
import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import SidebarCard from "./SidebarCard.js";

export default class Sidebar extends React.Component {
    createPlcList(){
        let ids = [1, 2, 3, 4, 5, 6];
        const plcList = [];
        for(let i = 0; i <= ids.length; i++){
            plcList.push(
                <Row bsPrefix="popupContent">
                    PLC ID: {i}
                </Row>
            );
        }
        return plcList;
    }

    createConErrList(){
        let ids = [1, 2, 3, 4, 5, 6];
        const errorList = [];
        for(let i = 0; i <= ids.length; i++){
            errorList.push(
                <Row bsPrefix="popupContent">
                    <p>
                        PLC ID: {i}     ERROR: Lost connection to PLC Host
                    </p>
                </Row>
            );
        }
        return errorList;
    }

    create

    render(){
        const plcList = this.createPlcList();
        const conErrList = this.createConErrList();

        return(
            <Container>
                <SidebarCard title={"Linked PLC's"} content={plcList}>
                    infoList
                </SidebarCard>
                <SidebarCard title={"Connection Errors"} content={conErrList}>
                    infoList
                </SidebarCard>
                <SidebarCard title={"Recent Events"} content={"No Recent Events"}>
                    infoList
                </SidebarCard>
                <SidebarCard title={"Sent Commands"} content={"No Sent Commands"}>
                    infoList
                </SidebarCard>
                <SidebarCard title={"Error Logs"} content={"No PLC Errors"}>
                    infoList
                </SidebarCard>

            </Container>
        )
    }
}