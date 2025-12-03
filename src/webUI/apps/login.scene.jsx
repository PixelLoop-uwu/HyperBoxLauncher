const { useState, useEffect } = React;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function Login ({ setScene }) {
  const [visible, setVisible] = useState(false);

  const [login, setLogin] = useState('');
  const [token, setToken] = useState('');

  const [incorrect, setIncorrect] = useState(false);
  const [serverError, setServerError] = useState(false);
  const [isDisabled, isDisabledToggle] = useState(false);

  const [loginOpacity, setLoginOpacity] = useState(1);

  const [connectionError, setConnectionError] = useState(false);
  const [connectionErrorCounter, setConnectionErrorCounter] = useState(0);

  useEffect(() => {
    async function connectionCheck() {
      if (!await window.pywebview.api.connectionCheck())
        setConnectionError(true)
    }

    async function fetchOptions() {
      const [lastedLogin, lastedToken] = await window.pywebview.api.getLastOptions();
      setLogin(lastedLogin);
      setToken(lastedToken);
    }

    connectionCheck()
    fetchOptions();
  }, [])

  async function tryToLogin() {
    if (window.pywebview?.api) {
      setLoginOpacity(0.8)
      isDisabledToggle(true)
      
      const status = await window.pywebview.api.tryToLogin(login, token);

      setLoginOpacity(1)
      isDisabledToggle(false)
        
      if ("error" in status) {
        if (status.status === "token_or_username_is_incorrect" || status.status === "token_or_username_is_invalid") {
          incorrectLoginOrTokenState();
        }

        else if (status.status == "error") {
          serverErrorState()

          if (connectionErrorCounter >= 2) 
            setConnectionError(true)

          setConnectionErrorCounter(connectionErrorCounter + 1)
        }
      }

      if (status.status == true) setScene("main")
  }}
  
  async function incorrectLoginOrTokenState () {
    setIncorrect(true); 
    isDisabledToggle(true); 

    await sleep(2000); 

    isDisabledToggle(false);
    setIncorrect(false);
  }

  async function serverErrorState () {
    setServerError(true); 
    isDisabledToggle(true);
    setLoginOpacity(0.8)

    await sleep(5000); 

    setServerError(false);
    isDisabledToggle(false);
    setLoginOpacity(1)
  }

  return (
    <main className='auth-LoginScene'>

      {connectionError && 
        <ErrorOverlay 
          errorTitle="Ошибка подключения" 
          errorLog="Повторите попытку через некоторое время или обратитесь в тикет" 
        />
      }


      <div className="auth-content">
        <img src="../assets/logo.png" className="auth-logo" />

        <div className="auth-title">HyperBox Launcher</div>
        <div className="auth-sub-title">Введите логин и токен, чтобы продолжить</div>

        <input 
          type="text"
          value={login}
          placeholder="Логин" 
          className="auth-input" 
          onChange={(e) => setLogin(e.target.value)} 
        />

        <input 
          type={visible ? "text" : "password"}
          value={token}
          placeholder="Токен" 
          className={`auth-input ${incorrect ? "incorrect" : ""}`}
          id='auth-password'
          onChange={(e) => setToken(e.target.value)} 
        />
        
        <button 
          type="button" 
          className="auth-button" 
          id="auth-button"
          onClick={tryToLogin}
          style={{opacity: loginOpacity}}
          disabled={isDisabled}
        >Войти</button>

        {serverError ? <span className="auth-error">Не удается получить доступ к серверу</span> : ''}
      </div>
    </main>
  )
}