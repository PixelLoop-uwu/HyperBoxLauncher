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

  useEffect(() => {
    async function fetchOptions() {
      const [lastedLogin, lastedToken] = await window.pywebview.api.getLastOptions();
      setLogin(lastedLogin);
      setToken(lastedToken);
    }
    fetchOptions();
  }, []);

  async function tryToLogin() {
    if (window.pywebview?.api) {
      const status = await window.pywebview.api.tryToLogin(login, token);
        
      if ("error" in status) {
        if (status.error == "token_or_username_is_incorrect") {

        } else if (status.error == "token_or_username_is_invalid") {

        } else if (status.error == "connection_error") {

        }
      }

      if (status.status) {
        setScene("main")
      }
  }};
  
  async function incorrectPasswordState() {
    setIncorrect(true); await sleep(2000); setIncorrect(false)
  }

  return (
    <main className='auth-LoginScene'>
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
        >Войти</button>

        {serverError ? <span className="auth-error">Не удается получить доступ к серверу :(</span> : ''}
      </div>
    </main>
  );
}