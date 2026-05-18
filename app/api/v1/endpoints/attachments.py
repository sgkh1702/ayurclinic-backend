{visit.attachments?.length > 0 && (
  <div className="history-visit-box">
    <div className="history-visit-box-title">Attachments</div>
    <div className="history-attachment-list">
      {visit.attachments.map((att) => (
        <a
          key={att.id}
          href={att.file_url}
          target="_blank"
          rel="noopener noreferrer"
          className="visit-paper-link"
        >
          {att.file_name}
        </a>
      ))}
    </div>
  </div>
)}