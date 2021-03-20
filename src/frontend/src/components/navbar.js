import React from 'react';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import styled from 'styled-components';
import logo from "../SUTDLogo 1.png";
import {clearToken} from "../variables/auth";

const Styles = styled.div`
  .navbar {
    background-color: #F3F6FA;
  }

  a, .navbar-nav, .navbar-light .nav-link {
    color: #3C64B1;

    &:hover {
      color: #322d2d;
    }
  }

  .navbar-brand {
    font-size: 1.4em;
    color: #9FFFCB;

    &:hover {
      color: #322d2d;
    }
  }

  .form-center {
    position: absolute !important;
    left: 25%;
    right: 25%;
  }
`;

export const NavigationBar = () => (
    <Styles>
        <Navbar expand="lg">
            <Navbar.Brand href="/"><img src={logo} alt="SUTD Housing Portal" width={"50%"}/></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Item><Nav.Link href="/profile">Profile</Nav.Link></Nav.Item>
                    <NavDropdown title="Events">
                        <NavDropdown.Item href="/event_history">Event History</NavDropdown.Item>
                        <NavDropdown.Item href="/event">Upcoming Events</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="/event_creation">Create Event</NavDropdown.Item>
                        <NavDropdown.Item>View Event</NavDropdown.Item>
                    </NavDropdown>
                    <NavDropdown title="Application">
                        <NavDropdown.Item href="/application_status">Check Status</NavDropdown.Item>
                        <NavDropdown.Item href="/apply">Housing Application</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="/application_creation">Create Application</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Item><Nav.Link href="/logout" onClick = {clearToken}>Logout</Nav.Link></Nav.Item>
                    <Nav.Item><Nav.Link href="/">Home</Nav.Link></Nav.Item>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    </Styles>
)
