function SummaryCard({ summary }) {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        🤖 AI Investment Summary
      </h2>

      {summary ? (
        <p>{summary.summary}</p>
      ) : (
        <p>Summary will appear here.</p>
      )}
    </div>
  );
}

export default SummaryCard;