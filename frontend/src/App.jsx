import { useState } from "react";

function App() {
    const [query, setQuery] = useState("");
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);

    const sourceColors = {
        "Google News": "bg-blue-100 text-blue-800",
        "SEBI": "bg-red-100 text-red-800",
        "RBI": "bg-green-100 text-green-800",
        "CBI": "bg-yellow-100 text-yellow-800",
        "MCA": "bg-purple-100 text-purple-800",
    };

    const fetchNews = async () => {
        setLoading(true);
        setArticles([]);
        try {
            const res = await fetch("http://localhost:5000/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });
            const data = await res.json();

            // ✅ backend returns an array, not { articles: [...] }
            let items = Array.isArray(data) ? data : data.articles || [];

            // ✅ sort newest first if pubDate exists
            items = items.sort((a, b) => {
                if (!a.pubDate || !b.pubDate) return 0;
                return new Date(b.pubDate) - new Date(a.pubDate);
            });

            setArticles(items);
        } catch (err) {
            console.error("Error fetching news:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
                📰 Negative News Checker
            </h1>

            {/* Search bar */}
            <div className="flex justify-center mb-6">
                <input
                    type="text"
                    className="p-3 rounded-l-xl border w-96 shadow"
                    placeholder="Enter company or person name..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button
                    onClick={fetchNews}
                    className="px-6 py-3 bg-blue-600 text-white rounded-r-xl hover:bg-blue-700"
                >
                    Search
                </button>
            </div>

            {/* Loader */}
            {loading && (
                <div className="flex justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                </div>
            )}

            {/* Results */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {articles.map((a, i) => (
                    <div
                        key={i}
                        className="bg-white p-5 rounded-2xl shadow hover:shadow-lg transition"
                    >
                        <div className="flex justify-between items-start mb-2">
                            <h2 className="font-semibold text-lg">{a.title}</h2>
                            <span
                                className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${sourceColors[a.source] || "bg-gray-200 text-gray-800"
                                    }`}
                            >
                                {a.source || "Unknown"}
                            </span>
                        </div>
                        <p className="text-sm text-gray-400 mb-3">{a.pubDate}</p>
                        <a
                            href={a.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                        >
                            🔗 Read More
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;

