import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

const BenfordAnalysisPage = () => {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalysisData();
  }, []);

  const fetchAnalysisData = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/get-benford-data");
      const data = await response.json();
      console.log("Benford analysis response:", data); // Debug log

      if (data.status === "success") {
        const benfordData = data.benford_data;
        console.log("Benford data:", benfordData); // Debug log

        // Transform data for chart
        const chartData = Array.from({ length: 9 }, (_, i) => ({
          digit: i + 1,
          actual: benfordData.actual_distribution[i],
          expected: benfordData.expected_distribution[i],
        }));

        setAnalysisData({
          ...benfordData,
          risk_level:
            benfordData.similarity_score < 0.5
              ? "high"
              : benfordData.similarity_score < 0.8
              ? "moderate"
              : "normal",
          chartData,
          summary: data.summary, // Add the summary to the state
        });
      } else if (data.status === "empty") {
        console.log("No tax data available"); // Debug log
        setError("No tax data available for analysis");
      } else {
        console.error("Error in response:", data.error); // Debug log
        setError(data.error || "Failed to fetch analysis data");
      }
    } catch (err) {
      console.error("Fetch error:", err); // Debug log
      setError("Failed to fetch analysis data");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case "high":
        return "text-red-600";
      case "moderate":
        return "text-yellow-600";
      default:
        return "text-green-600";
    }
  };

  const getRiskIcon = (riskLevel) => {
    if (riskLevel === "normal") {
      return <CheckCircleIcon className="h-8 w-8 text-green-600" />;
    }
    return (
      <ExclamationTriangleIcon
        className={`h-8 w-8 ${getRiskColor(riskLevel)}`}
      />
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-600">
        <ExclamationTriangleIcon className="h-12 w-12 text-gray-400 mb-4" />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="h-full p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-2xl font-semibold mb-4">Benford's Law Analysis</h1>

        <div className="mb-6">
          <div className="flex items-center space-x-4 mb-4">
            {getRiskIcon(analysisData.risk_level)}
            <div>
              <h2 className="text-xl font-medium">
                Risk Level:{" "}
                <span className={getRiskColor(analysisData.risk_level)}>
                  {analysisData.risk_level.charAt(0).toUpperCase() +
                    analysisData.risk_level.slice(1)}
                </span>
              </h2>
              <p className="text-gray-600">
                Similarity Score:{" "}
                {(analysisData.similarity_score * 100).toFixed(2)}%
              </p>
            </div>
          </div>

          <p className="text-gray-600">
            {analysisData.risk_level === "normal"
              ? "The data follows Benford's Law closely, suggesting normal financial patterns."
              : analysisData.risk_level === "moderate"
              ? "Some deviation from Benford's Law detected. Moderate risk of irregular patterns."
              : "Significant deviation from Benford's Law detected. High risk of irregular patterns."}
          </p>
        </div>

        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={analysisData.chartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="digit"
                label={{ value: "", position: "bottom" }}
              />
              <YAxis
                label={{
                  value: "Frequency",
                  angle: -90,
                  position: "insideLeft",
                }}
              />
              <Tooltip />
              <Legend />
              <Bar dataKey="actual" name="Actual Distribution" fill="#4f46e5" />
              <Bar
                dataKey="expected"
                name="Expected (Benford's Law)"
                fill="#e5e7eb"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI-Generated Summary */}
        {analysisData.summary && (
          <div className="mt-6 bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              AI Analysis Summary
            </h3>
            <p className="text-gray-600 whitespace-pre-line">
              {analysisData.summary}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BenfordAnalysisPage;
