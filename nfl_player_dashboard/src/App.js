import React, { useEffect, useState, PureComponent } from "react";
import logo from "./logo.svg";
import "./App.css";
import BarChart from "./components/BarChart";
import SearchInput from "./components/searchInput";
import PlayerResults from "./components/PlayerResults";
import filterPlayer from "./components/filterPlayer";

// function App() {
//   // const [players, setPlayer] = useState([]);

//   // useEffect(() => {
//   //   fetch("/").then(response =>
//   //     response.json().then(data => {
//   //       // setPlayer(data);
//   //       console.log(data);
//   //     })
//   //   );
//   // }, []);

//   // constructor(props) {
//   //   super(props);
//   //   this.state = {
//   //     filteredPlayer: filterPlayer("", 5)
//   //   };
//   // }

//   // constructor(){
//   //   super();
//   // }

//   // handleSearchChange = event => {
//   //   this.setState({
//   //     filteredPlayer: filterPlayer(event.target.value, 20)
//   //   });
//   // };

//   return (
//     <div className="App">
//       {/* <SearchInput textChange={this.handleSearchChange} /> */}
//       <SearchInput />
//       {/* <SearchInput textChange={this.handleSearchChange} /> */}
//       {/* <PlayerResults playerData={this.state.filteredPlayer} /> */}

//       {/* <Players players={players} /> */}
//       <BarChart
//       // data={this.state.data}
//       // width={this.state.width}
//       // height={this.state.height}
//       />
//     </div>
//   );
// }

// export default App;

export default class App extends PureComponent {
  // state = {
  //   selectedOption: null
  // };

  constructor(props) {
    super(props);
    this.state = {
      filteredPlayer: filterPlayer("", 30),
      selectedOption: "P.Manning"
    };
  }

  handleSelect = selectedOption => {
    this.setState({ selectedOption });
    console.log(this.state.selectedOption);
  };

  handleSearchChange = event => {
    this.setState({
      filteredPlayer: filterPlayer(event.target.value, 20)
    });
  };

  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-sm-2 d-none d-md-block bg-light sidebar">
            <div className="sidebar-sticky" id="sidebar">
              <SearchInput textChange={this.handleSearchChange} />
              <PlayerResults
                playerData={this.state.filteredPlayer}
                onSelect={this.handleSelect}
              />
            </div>
          </div>
          {/* <div className="col-sm-8" id="chartbox">
            <BarChart />
          </div> */}
          <main role="main" className="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
            <div className="chartjs-size-monitor">
              <div className="chartjs-size-monitor-expand"></div>
              <div className="chartjs-size-monitor-shrink"></div>
            </div>

            <h2>Summary Statistics</h2>
            <div className="table-responsive" id="summary-table"></div>
            <h1 className="h2">Player Performance over Time</h1>
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
              <div
                className="my-4 chartjs-render-monitor"
                id="chartbox"
                width="622"
                height="262"
              >
                <BarChart />
              </div>
            </div>
          </main>
        </div>
      </div>
    );
  }
}
