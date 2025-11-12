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
  const [maxRam, setMaxRam] = useState(1024)

  const [logMenuOpen, setLogMenuOpen] = useState(false);
  
  useEffect(() => {
    async function getMainData() {
      const modpacks = await window.pywebview.api.getMainData();
      const settings = await window.pywebview.api.getLauncherSettings();

      setData(modpacks);

      setFullscreenOption(settings.fullscreen);
      setDebugOption(settings.debug);
      setMainDir(settings.mainDir);
      
      setMaxRam(settings.maxRam);
      setRamOption(settings.ram);
      setRamSliderValue(settings.ram / 1024);
    }; getMainData();
  }, []);

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
  };

  const modpackTemplate = (modpackInfo) => (
    <div
    key={modpackInfo.id}
    className={`modpack-card ${modpackInfo.id === currentModpack ? 'active' : ''}`}
    onClick={() => handleClickModpack(modpackInfo.id)}
    >
      <img src="" alt="" />
      <span className="version">{modpackInfo.version}</span>
      <span className="name">{modpackInfo.title}</span>
    </div>
  );
  
  const ramInputCheck = (e) => {
    let value = parseInt(e.target.value);

    if (value > maxRam) value = maxRam;
    else if (value < 1024) value = 1024;

    setRamOption(value);
    setRamSliderValue(value / 1024);
  };

  const ramSliderCheck = (e) => {
    let value = parseInt(e.target.value) * 1024;

    if (value > maxRam) value = maxRam;
    else if (value < 1024) value = 1024;

    setRamOption(value);
    setRamSliderValue(value / 1024);
  };

  const ramSliderHandler = (e) => {
    const value = parseInt(e.target.value) * 1024;
    setRamSliderValue(e.target.value);
    setRamOption(value);
  };

  const saveLauncherSettings = async () => {
    const settings = {mainDir: mainDir, ramOption: ramOption}

    await window.pywebview.api.saveLauncherSettings(settings)
    setSettingsOpen(false)
  };

  const openGameFolder = async () => {
    if (!current) return;
    await window.pywebview.api.openGameFolder(current.folder);
  };

  const chooseGameFolder = async () => {
    if (!current) return;
    const folder = await window.pywebview.api.chooseGameFolder();

    setMainDir(folder.replace(/\\/g, "/") + "/HyperBox")
  };

  const launchPlay = async (modpack_id) => { 
    await window.pywebview.api.launchPlay(modpack_id)
  };

  const current = data ? data.modpacks[currentModpack] : null;

  return (
    <main className="MainScene">
      <div className="main-modpacks-list">
        {data ? data.modpacks.map(m => modpackTemplate(m)) : 'Загрузка...'}
      </div>

      <div className="main-content">
          <button className="main-settings-toggle" onClick={() => setSettingsOpen(true)}>
            <img src="../assets/main/settings_icon.png" alt=""/>
          </button>

        <span className={`main-title ${animationClass}`}>
          {current ? current.title : 'Загрузка...'}
        </span>

        <span className={`main-description ${animationClass}`}>
          {current ? current.description.map((p, index) => <p key={index}>{p}</p>) : 'Загрузка...'}
        </span>

        <div className="main-control">
          <button type="button" className="main-play" onClick={launchPlay(currentModpack)}>Играть</button>
          <button
            type="button"
            className="main-folder"
            onClick={ openGameFolder }
          >
            <img src="../assets/main/folder_icon.png" alt="" />
          </button>

          <div className="main-auth">
            <label>
              <img src="../assets/main/imsteeve.jpg" alt="avatar" />
              <input type="file" name="skin" hidden />
            </label>
            <span>{data ? data.username : 'Загрузка...'}</span>
          </div>
        </div>
      </div>

    {settingsOpen && (
      <div className="settings-overlay" onClick={ saveLauncherSettings }>
        <div className="settings-content" onClick={e => e.stopPropagation()}>
          <h2 className="settings-title">Настройки</h2>

          <div className="settings-section">
              <div className="settings-ram-info">
                Память (RAM):
                <label className="settings-label">
                  <input
                    type="number"
                    min="1024"
                    max={maxRam}
                    step="256"
                    value={ramOption}
                    onChange={(e) => setRamOption(parseInt(e.target.value))}
                    onBlur={ramInputCheck}
                  />
                  Mb
                </label>
              </div>

              <input
                className="settings-memory-slider"
                type="range"
                min="0"
                max={Math.ceil(maxRam / 1024)}
                value={ramSliderValue}
                onChange={ramSliderHandler}
                onBlur={ramSliderCheck}

                style={{
                  background: maxRam
                    ? `linear-gradient(90deg, var(--main-color) ${(ramSliderValue * 1024) / maxRam * 100}%, #333 ${(ramSliderValue * 1024) / maxRam * 100}%)`
                    : '#333'
                }}
              />
            </div>

          <div className="settings-section-2">
            <div className="settings-path-title">Основная дериктория:</div>
            <div className="settings-path-container">
              <label onClick={ openGameFolder }>
                <img src="../assets/main/folder_icon.png" alt="" />
                <span className="settings-path">{mainDir && mainDir.length > 35 ? mainDir.slice(0, 35) + "..." : mainDir}</span>
              </label>

              <button className="settings-change-path" type="button" onClick={chooseGameFolder}>
                <img src="../assets/main/pencil.png" alt="" />
              </button>
            </div>
          </div>

          <button className="settings-close" onClick={saveLauncherSettings} type="button">Сохранить</button>
        </div>
      </div>
    )}

    {logMenuOpen && (
      <div className="logmenu-overlay">
        
      </div>
    )}
    </main>
  );
}
