function Loading ( { title } ) {
  return (
    <div className="loading_overlay">
      <div className="loading-title">{title}</div>

      <div className="loading-dots-container">
        <span className="loading-dot"></span>
        <span className="loading-dot"></span>
        <span className="loading-dot"></span>
			</div>
    </div>
  )
}