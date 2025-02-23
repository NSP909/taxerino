import { useState, useEffect } from "react";
import { AnalysisService } from "../services/analysisService";
import {
  ArrowPathIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";

export default function BenfordPage() {
  const [benfordData, setBenfordData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchBenfordData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await AnalysisService.getBenfordAnalysis();
      setBenfordData(data);
    } catch (error) {
      console.error("Failed to fetch Benford analysis:", error);
      setError("Failed to load Benford analysis");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBenfordData();
  }, []);

  return (
    <div className="h-full p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">
            Benford's Law Analysis
          </h1>
          <p className="text-base text-emerald-600 mt-1">
            Statistical analysis of your financial data patterns
          </p>
        </div>
        <button
          onClick={fetchBenfordData}
          disabled={loading}
          className={`inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${
              loading
                ? "bg-emerald-100 text-emerald-400 cursor-not-allowed"
                : "bg-emerald-50 text-emerald-600 hover:bg-emerald-100"
            }`}
        >
          <ArrowPathIcon
            className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`}
          />
          {loading ? "Refreshing..." : "Refresh Analysis"}
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-emerald-900/10 p-6">
        {error ? (
          <div className="text-center py-10">
            <ExclamationCircleIcon className="h-14 w-14 text-red-200 mx-auto mb-4" />
            <p className="text-lg text-red-900 font-medium">{error}</p>
            <button
              onClick={fetchBenfordData}
              className="mt-4 text-sm text-emerald-600 hover:text-emerald-700"
            >
              Try again
            </button>
          </div>
        ) : loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-pulse flex space-x-2">
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            </div>
          </div>
        ) : benfordData ? (
          <div className="space-y-6">
            <div className="bg-emerald-50 rounded-lg p-6">
              <h3 className="text-lg font-medium text-emerald-900 mb-4">
                Analysis Results
              </h3>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <h4 className="text-sm font-medium text-emerald-800">
                      Similarity Score
                    </h4>
                    <p className="text-2xl font-bold text-emerald-600 mt-2">
                      {(benfordData.similarity_score * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <h4 className="text-sm font-medium text-emerald-800">
                      Risk Level
                    </h4>
                    <p
                      className={`text-2xl font-bold mt-2 ${
                        benfordData.similarity_score >= 0.8
                          ? "text-green-600"
                          : benfordData.similarity_score >= 0.5
                          ? "text-yellow-600"
                          : "text-red-600"
                      }`}
                    >
                      {benfordData.similarity_score >= 0.8
                        ? "Low"
                        : benfordData.similarity_score >= 0.5
                        ? "Medium"
                        : "High"}
                    </p>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <h4 className="text-sm font-medium text-emerald-800 mb-2">
                    Analysis Summary
                  </h4>
                  <p className="text-sm text-emerald-700">
                    {benfordData.summary}
                  </p>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <h4 className="text-sm font-medium text-emerald-800 mb-2">
                    First Digit Distribution
                  </h4>
                  <div className="h-64">
                    {/* Add chart visualization here if needed */}
                    <pre className="text-xs text-emerald-600 overflow-auto">
                      {JSON.stringify(benfordData.first_digits, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-10">
            <p className="text-lg text-emerald-900 font-medium">
              No Benford analysis available
            </p>
            <p className="text-base text-emerald-600 mt-2">
              Upload tax documents to generate analysis
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
