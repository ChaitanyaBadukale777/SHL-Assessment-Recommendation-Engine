export default function ResultCard({ item }) {
  return (
    <div style={{
      border: "1px solid #ddd",
      padding: "16px",
      marginBottom: "12px",
      borderRadius: "8px"
    }}>
      <h3>{item.name}</h3>

      <p><strong>Duration:</strong> {item.duration} mins</p>
      <p><strong>Test Type:</strong> {item.test_type.join(", ")}</p>
      <p><strong>Remote Support:</strong> {item.remote_support}</p>

      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
      >
        View Assessment
      </a>
    </div>
  );
}
