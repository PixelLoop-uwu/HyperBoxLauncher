const root = ReactDOM.createRoot(document.getElementById('root'));
const { useState, useEffect } = React;

function App () {
  const [scene, setScene] = useState("login");
  
  useEffect(() => {
    const handler = () => {
      console.log("[Hyperbox] PyWebView is ready");
    };

    window.addEventListener("pywebviewready", handler);

    return () => {
      window.removeEventListener("pywebviewready", handler);
    };
  }, []);

  const closeWindow = () => {
    if (window.pywebview?.api) {
      window.pywebview.api.close();
    }
  };

  const minimizeWindow = () => {
    if (window.pywebview?.api) {
      window.pywebview.api.minimize();
    }
  };

  const changeSceneToMain = () => {
    setScene("main")
  }
 
  return (
    <>
      <header className="pywebview-drag-region">
        <div className="window-title">HyperBox Launcher</div>
        <div className="action-buttons">
          <div id="window-minimize" onClick={minimizeWindow}>-</div>
          <div id="window-close" onClick={closeWindow}>⨯</div>
        </div>
      </header>

      {scene == "login" ? <Login changeSceneToMain = {changeSceneToMain} /> : <Main />}
      {/* {scene == "main" && <Main />} */}

    </>
  )
}

root.render( <App /> );