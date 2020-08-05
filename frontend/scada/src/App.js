import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col} from 'react-bootstrap';
import Sidebar from "./Sidebar/Sidebar.js";
import MainDisplay from "./MainDisplay/MainDisplay.js";

function App() {
  const style = {
    width: "98%",
    maxWidth: "none",
  };
  return (

    <div className="App">

      <header className="App-header">
        <Container style={style}>
          <Row>
            <Col>
              <Sidebar/>
            </Col>
            <Col xs={10}>
              <MainDisplay/>
            </Col>
          </Row>
        </Container>
      </header>
    </div>
  );
}

export default App;
