import {Card, Button, Row} from "react-bootstrap";
import React from "react";
import Popup from "reactjs-popup";
import 'bootstrap/dist/css/bootstrap.min.css';
import './sidebar.css';

export default class SidebarCard extends React.Component {

    render() {
        return (
            <Card bg={'secondary'} text={'light'}>
                <Card.Title>
                    {this.props.title}
                </Card.Title>
                <Card.Body >
                    <Row bsPrefix="buttonBody">
                        <Popup modal trigger={<Button variant="info">View {this.props.title}</Button>} position="right center">
                            <div className="sidbarText">
                                {this.props.content}
                            </div>
                        </Popup>
                    </Row>
                </Card.Body>
            </Card>
        )
    }
}