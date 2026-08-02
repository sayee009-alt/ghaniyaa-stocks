function Watchlist({ watchlist }) {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        ❤️ My Watchlist
      </h2>

      {!watchlist || watchlist.length === 0 ? (
        <p>No stocks added yet.</p>
      ) : (
        <ul className="list-disc ml-6">
          {watchlist.map((stock, index) => (
            <li key={index}>{stock}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Watchlist;