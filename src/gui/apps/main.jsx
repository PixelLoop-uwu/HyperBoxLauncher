const { useState, useEffect } = React;

function Main () {
  const [data, setData] = useState(null)

  const [currentModpack, setCurrentModpack] = useState(0)

  useEffect(() => {
    async function getMainData() {
      const response = await window.pywebview.api.getMainData();
      setData(response)
    }
    getMainData();
  }, []);

  const modpackTemplate = (modpackInfo) => (
    <div className="modpack-card" onClick={() => {setCurrentModpack(modpackInfo.id)}}>
      <img src="" />
      <span className="version">{modpackInfo.version}</span>
      <span className="name">{modpackInfo.title}</span>
    </div>
  )


  return (
    <main className="MainScene">
      <div className="main-modpacks-list">
        {data ? data.modpacks.map(m => modpackTemplate(m)) : 'Загрузка...'}
      </div>

      <div className="main-content">
        <button className="main-settings-toggle">
          <img src="../assets/main/settings_icon.png" alt="" />
        </button>
      
        <span className="main-title">{data ? data.modpacks[currentModpack].title : 'Загрузка...'}</span>

        <span className="main-description">
          {data ? data.modpacks[currentModpack].description.map((p, index) => (
            <p key={index}>{p}</p> 
          )) : 'Загрузка...'}
        </span>

        <div className="main-control">
          <button type="button" className="main-play">
            {/* <img src="../assets/main/play_icon.png" alt="" />  */} Играть
          </button>
          <button type="button" className="main-folder" 
              onClick={ async () => {
                await window.pywebview.api.openGameFolder(data.modpacks[currentModpack].folder)
              }}>
            <img src="../assets/main/folder_icon.png" alt="" />
          </button>
        
          <div className="main-auth">
            <label>
              <img src="../assets/main/imsteeve.jpg"/>
              <input type="file" name="skin" hidden />
            </label>
            <span>{data ? data.username : 'Загрузка...'}</span>
          </div>
        </div>

        <div className="main-content-2">
          <div className="main-progress-bar">
            <div className="main-progress"></div>
          </div>
          <span className="main-progress-logs">Сосал сосал сосал</span>
        </div>
      </div>
        
        {/* Settings */}

      <div className="settings-overlay">
        <div className="settings-content">
          <div className="settings-title">Настройки</div>

          <div className="settings-memory-content">
            <input type="range"  />
          </div>
        </div>
      </div>
    </main>
  )
}
