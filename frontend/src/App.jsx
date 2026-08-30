import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [trend, setTrend] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = () => {
      axios
        .get("https://donation-dashboard-production.up.railway.app/dashboard/summary")
        .then((res) => {
          setSummary(res.data);
          setError(null);
        })
        .catch((err) => setError(err.message));

      axios
        .get("https://donation-dashboard-production.up.railway.app/dashboard/trend")
        .then((res) => {
          const formatted = res.data.points.map((p) => ({
            date: p.date,
            total: parseFloat(p.total),
          }));
          setTrend(formatted);
        })
        .catch((err) => setError(err.message));
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (error) return <div className="dashboard">Error loading dashboard: {error}</div>;
  if (!summary || !trend) return <div className="dashboard">Loading dashboard...</div>;

  const progress = summary.donation_progress_pct ?? 0;

  return (
    <div className="dashboard">
      <h1>Donation Dashboard</h1>

      <div className="cards">
        <div className="card">
          <h3>Total Donors</h3>
          <p>{summary.total_donors}</p>
        </div>
        <div className="card">
          <h3>Total Donated</h3>
          <p>${summary.total_donated}</p>
        </div>
        <div className="card">
          <h3>Target Amount</h3>
          <p>${summary.target_amount ?? "N/A"}</p>
        </div>
        <div className="card">
          <h3>Donor Engagement</h3>
          <p>{summary.repeat_donor_pct}%</p>
        </div>
      </div>

      <div className="progress-section">
        <h3>Donation Progress</h3>
        <div className="progress-bar-track">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
        <div className="progress-label">
          {progress}% of ${summary.target_amount ?? "N/A"} raised
        </div>
      </div>

      <div className="chart-section">
        <h3>Donation Trend</h3>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={trend}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="total"
              stroke="#6c5ce7"
              strokeWidth={3}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;