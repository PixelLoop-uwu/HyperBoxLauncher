const { useState, useEffect } = React;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function GameLogOverlay() {
	const [stage, setStage] = useState('Загрузка...')

	const [currentFile, setFile] = useState('Загрузка...')
	const [maxProgress, setMaxProgress] = useState(1)
	const [progress, setProgress] = useState(0)

	const [errorTitle, setErrorTitle] = useState("")
	const [errorSubtitle, setErrorSubtitle] = useState("")

	const [isError, setError] = useState(false)
	const [isOpenOverlay, setOpenOverlay] = useState(true)

	const ChangeProgress = (count) => {
		setProgress(prev => prev + count)
	}

	const ResetProgress = () => {
		setProgress(0)
	}

	const ChangeMaxProgress = (progress) => {
		setMaxProgress(progress)
	}

	const ChangeStage = (stage) => {
		setStage(stage)
	}

	const ChangeCurrentFile = (file) => {
		setFile(file)
	}

	const Error = (title, subtitle) => {
		setErrorTitle(title)
		setErrorSubtitle(subtitle)
		setError(true)
		sleep(1000)
		setOpenOverlay(false)
	}

	useEffect(() => {
		window.GameLog = {
			addProgress: ChangeProgress,
			setMaxProgress: ChangeMaxProgress,
			setStage: ChangeStage,
			setCurrentFile: ChangeCurrentFile,
			resetProgress: ResetProgress,
			setErrorr: Error
		}
	}, [])


	return (
		<>
			{isOpenOverlay && <div className="overlay">
				<div className="gameLogs-content">
					<div className="gameLog-title">Запуск игры...</div>

					<div className="gameLog-status-container">
						<span className="gameLog-status">{stage}</span>

						<div className="gameLog-progressbar">
							<div className="gameLog-progress"
								style={{width: `${(progress / maxProgress) * 100}%`}}
							></div>
						</div>

						<div className="gameLog-logs-container">
						<span className="gameLog-logs-file">{currentFile}</span>
							<span className="gameLog-logs-progress">{progress} / {maxProgress}</span>
						</div>
					</div>

					<div className="gameLog-dots-container">
						<span className="gameLog-dot"></span>
						<span className="gameLog-dot"></span>
						<span className="gameLog-dot"></span>
					</div>

					{/* optional close button in future
					<button className="gameLog-kill-button" onClick={onClose}>Завершить</button>
					*/}
				</div>
			</div>}

			{isError && <ErrorOverlay 
        errorTitle={errorTitle}
        errorLog={errorSubtitle} 
      />}
		</>
	);
}

