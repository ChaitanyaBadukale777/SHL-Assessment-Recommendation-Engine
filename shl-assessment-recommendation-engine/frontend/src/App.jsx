import { useState } from "react";
import axios from "axios";
import ResultCard from "./components/ResultCard";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRecommend = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/recommend",
        {
          query,
          top_k: 10,
        }
      );

      setResults(response.data.recommended_assessments);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch recommendations");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "900px", margin: "40px auto" }}>
      <h1>SHL Assessment Recommendation Engine</h1>

      <textarea
        rows="4"
        placeholder="Enter job description or query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", padding: "10px", fontSize: "16px" }}
      />

      <button
        onClick={handleRecommend}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Recommend
      </button>

      {loading && <p>Loading recommendations...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.map((item, idx) => (
        <ResultCard key={idx} item={item} />
      ))}
    </div>
  );
}

export default App;
