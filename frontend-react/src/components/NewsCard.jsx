function NewsCard({ news }) {
  if (!news || news.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold mb-4">
          📰 Latest News
        </h2>
        <p>No news available.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        📰 Latest News
      </h2>

      {news.map((item, index) => (
        <div
          key={index}
          className="border-b last:border-0 py-3"
        >
          <h3 className="font-semibold">
            {item.title}
          </h3>

          <p className="text-sm text-gray-500">
            {item.source}
          </p>
        </div>
      ))}
    </div>
  );
}

export default NewsCard;