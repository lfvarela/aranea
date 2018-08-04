import React, {Component} from 'react'
import { Navbar } from "react-bootstrap";
import InputHandle from '../InputHandle/InputHandle.js';

class Header extends Component {
	constructor(props) {
    super(props);
  }

  render() {
  	return (
      <div className="Header-container">
        <h1> Aranea </h1>
      </div>
  	)
  }
}

export default Header;