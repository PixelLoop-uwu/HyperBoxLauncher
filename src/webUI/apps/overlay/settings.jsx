function SettingsOverlay({
  maxRam,
  mainDir,
  ramOption,
  ramSliderValue,
  setRamOption,
  setRamSliderValue,
  setMainDir,
  openGameFolder,
  onClose,
  current
}) {

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
    const settings = {mainDir: mainDir, ram: ramOption}

    await window.pywebview.api.saveLauncherSettings(settings)
    onClose()
  };

  const chooseGameFolder = async () => {
    if (!current) return;
    
    const folder = await window.pywebview.api.chooseGameFolder();
    if (!folder) return;

    setMainDir(folder.replace(/\\/g, "/") + "/HyperBox")
  };


  return (
    <div className="overlay" onClick={ saveLauncherSettings }>
        <div className="settings-content" onClick={e => e.stopPropagation()}>
          <div className="settings-title">Настройки игры</div>

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
                    ? `linear-gradient(90deg, var(--main-color) ${(ramSliderValue * 1024) / maxRam * 100}%, var(--gray) ${(ramSliderValue * 1024) / maxRam * 100}%)`
                    : '#333'
                }}
              />
            </div>

          <div className="settings-section-2">
            <div className="settings-path-title">Основная дериктория:</div>
            <div className="settings-path-container">
              <label onClick={ openGameFolder }>
                <img src="../assets/main/folder_icon.png" alt="" className="settings-folder-icon" />
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
    )
}