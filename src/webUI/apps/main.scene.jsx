const { useState, useEffect } = React;

function Main() {
  const [data, setData] = useState(null);
  const [currentModpack, setCurrentModpack] = useState(0);

  const [animating, setAnimating] = useState(false);
  const [animationClass, setAnimationClass] = useState('');

  const [settingsOpen, setSettingsOpen] = useState(false);

  const [fullscreenOption, setFullscreenOption] = useState(null);
  const [debugOption, setDebugOption] = useState(null);
  const [mainDir, setMainDir] = useState(null);

  const [ramOption, setRamOption] = useState(1024);
  const [ramSliderValue, setRamSliderValue] = useState(1024);
  const [maxRam, setMaxRam] = useState(1024);

  const [gameLogsOpen, setGameLogsOpen] = useState(false);

  const [connectionError, setConnectionError] = useState(false);
  
  
  useEffect(() => {
    async function getMainData() {
      const modpacks = await window.pywebview.api.getMainData();
      const settings = await window.pywebview.api.getLauncherSettings();
      
      if (modpacks.status == "error") {
        setConnectionError(true)
        return
      }

      setData(modpacks);

      setFullscreenOption(settings.fullscreen);
      setDebugOption(settings.debug);
      setMainDir(settings.mainDir);
      
      setMaxRam(settings.maxRam);
      setRamOption(settings.ram ? settings.ram : 1024);
      setRamSliderValue((settings.ram ? settings.ram : 1024) / 1024);
    }

    getMainData();
  }, [])

  const handleClickModpack = (id) => {
    if (!data || id === currentModpack || animating) return;

    const direction = id < currentModpack ? 'slideDown' : 'slideUp'; 
    setAnimationClass(direction);
    setAnimating(true);

    setTimeout(() => {
      setCurrentModpack(id);
      const enterDirection = direction === 'slideUp' ? 'slideDown' : 'slideUp';
      setAnimationClass(enterDirection);

      setTimeout(() => {
        setAnimationClass('');
        setAnimating(false);
      }, 300);
    }, 300);
  }

  const modpackTemplate = (modpackInfo) => (
    <div
    key={modpackInfo.id}
    className={`modpack-card ${modpackInfo.id === currentModpack ? 'active' : ''}`}
    onClick={() => handleClickModpack(modpackInfo.id)}
    >
      <span className="name">{modpackInfo.title}</span>
    </div>
  )


  const openGameFolder = async () => {
    if (!current) return;
    const path = mainDir + "/updates/" + current.folder;  

    await window.pywebview.api.openGameFolder(path);
  }

  const launchPlay = async (modpack) => { 
    setGameLogsOpen(true);
    changeConfigById("waiting")
    await window.pywebview.api.launchPlay(modpack);
  }

  const skinHandler = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = async (e) => {
      const base64Data = e.target.result.split(',')[1];
      await window.pywebview.api.uploadSkin(base64Data);
    };
    reader.readAsDataURL(file);
  }


  const current = data ? data.modpacks[currentModpack] : null;

  return (
    <main className="MainScene">
      {connectionError && 
        <ErrorOverlay 
          errorTitle="Ошибка подключения" 
          errorLog="Повторите попытку через некоторое время или обратитесь в тикет" 
        />
      }

      <div className="main-modpacks-list">
        {data ? data.modpacks.map(m => modpackTemplate(m)) : 'Loading'}
      </div>

      <div className="main-content">
          <button className="main-settings-toggle" onClick={() => setSettingsOpen(true)}>
            <img src="../assets/main/settings_icon.svg" alt=""/>
          </button>

        <span className={`main-title ${animationClass}`}>
          {current ? current.title : 'Loading'}
        </span>

        <span className={`main-description ${animationClass}`}>
          {current ? current.description.map((p, index) => <p key={index}>{p}</p>) : <p>Loading</p>}
        </span>

        <div className="main-control">
          <button type="button" className="main-play" onClick={() => {launchPlay(current.folder)}}>Играть</button>
          <button
            type="button"
            className="main-folder"
            onClick={ openGameFolder }
          >
            <img src="../assets/main/folder_icon.svg" alt="" />
          </button>

          <div className="main-auth">
            <label>
              <img src={`https://resources.hyperbox.world/player_data/${data && data.username}/avatar.png`} alt="" />
              <input type="file" name="skin" onChange={skinHandler} hidden />
            </label>
            <span>{data ? data.username : 'загрузка'}</span>
          </div>
        </div>
      </div>

    {settingsOpen && (
      <SettingsOverlay
        maxRam={maxRam}
        mainDir={mainDir}
        ramOption={ramOption}
        ramSliderValue={ramSliderValue}
        setRamOption={setRamOption}
        setRamSliderValue={setRamSliderValue}
        setMainDir={setMainDir}
        openGameFolder={openGameFolder}
        onClose={() => setSettingsOpen(false)}
        current={current}
      />
    )}

    {gameLogsOpen && (<GameLogOverlay />)}
    
    </main>
  );
}
