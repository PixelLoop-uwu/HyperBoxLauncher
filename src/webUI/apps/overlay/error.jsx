function ErrorOverlay({ errorTitle, errorLog }) {
  return (  
    <div className="error_overlay">
      <div className="error-content">
        <img src="../../assets/warning.svg" alt="" /> 

        <div className="error-container">
          <div className="error-title">{errorTitle}</div>
          <div className="error-log">{errorLog}</div>
        </div>
      </div>
    </div>
  )
}
