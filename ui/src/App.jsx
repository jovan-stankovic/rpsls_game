import React, {useEffect} from 'react';
import Game from "./components/Game.jsx";

function App() {
    useEffect(() => {
        document.title = "R-P-S-L-S";
      }, []);

  return (
    <div className="app-container">
     <Game />
    </div>
  );
}

export default App;
