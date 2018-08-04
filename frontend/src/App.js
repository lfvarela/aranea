import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import Graph from 'react-graph-vis';

import Header from './components/Header/Header.js'
import InputHandle from './components/InputHandle/InputHandle.js'
import UserGraph from './components/UserGraph/UserGraph.js'


class App extends Component {
  constructor(props) {
    super(props);

    const graph = {
      nodes: [
          {id: 1, label: 'Node 1'},
          {id: 2, label: 'Node 2'},
          {id: 3, label: 'Node 3'},
          {id: 4, label: 'Node 4'},
          {id: 5, label: 'Node 5'}
      ],
      edges: [
          {from: 1, to: 2},
          {from: 1, to: 3},
          {from: 2, to: 4},
          {from: 2, to: 5}
      ]
    } 

    const options = {
      layout: {
        hierarchical: true
      },
      edges: {
        color: "#000000"
      }
    }

    const events = {
      select: function(event) {
        var { nodes, edges } = event;
      }
    }

    this.state = {
      g: graph,
      o: options,
      e: events
    }
  }

  // processInputHandle(input){
  //   var handle = []
  //   for (var pair of input.entries()) {
  //     handle.push(pair[1]); 
  //     console.log(handle);
  //   }
  //   var graphOutput = createGraph(handle[0])

  //   this.setState({
  //     graphInfo: graphOutput
  //   })
  //   this.render()
  // }
          // <InputHandle inputCallback={i => this.setState({graphInfo: i})}></InputHandle>

  render() {
    return (
      <div class="graphContainer">
        <Graph graph={this.state.g} options={this.state.o} events={this.state.e} />
      </div>
    );
  }
}

function createGraph(formData){
  var xhr = new XMLHttpRequest();
  xhr.open('GET','/create_graph',true)
  xhr.onload = function (graph){
    var graphJSON = graph
    console.log(graphJSON)
    //do shit with this.graph
    return 'hi'

  }

  xhr.send(JSON.stringify({graph_type: "followers", root_underscore_node: formData, degree: 1}))
}

export default App;
