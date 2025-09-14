const root = ReactDOM.createRoot(document.getElementById('root'));
const { useState } = React;

function App () {
  const [scene, setScene] = useState("login");

  window.addEventListener('pywebviewready', () => {
  // Управление окном
    document.getElementById("window-close").onclick = () => window.pywebview.api.close();

    document.getElementById("window-minimize").onclick = () => window.pywebview.api.minimize();
  });

  return (
    <>
      <header class="pywebview-drag-region">
        <div class="window-title">HyperBox Launcher</div>
        <div class="action-buttons">
          <div id="window-minimize">-</div>
          <div id="window-close">⨯</div>
        </div>
      </header>

      
    </>
  )
}

root.render( <App /> );