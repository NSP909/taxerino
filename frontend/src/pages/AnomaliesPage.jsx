import React, { useState, useEffect } from "react";
import {
  ExclamationTriangleIcon,
  DocumentMagnifyingGlassIcon,
  ArrowPathIcon,
} from "@heroicons/react/24/outline";

const AnomalyCard = ({ title, data }) => {
  const { source_details, anomaly_details } = data;

  // Helper function to format value for display
  const formatValue = (value) => {
    if (typeof value === "object" && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-red-100 overflow-hidden">
      <div className="border-b border-red-100 bg-red-50/50 px-4 py-3">
        <h3 className="text-lg font-semibold text-red-900">{title}</h3>
      </div>
      <div className="p-4 space-y-4">
        {/* Source Details */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-2">
            Source Details
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(source_details).map(([source, details]) => (
              <div key={source} className="bg-gray-50 rounded-lg p-3">
                <div className="flex justify-between items-start">
                  <span className="text-sm font-medium text-gray-700">
                    {source}
                  </span>
                  <span className="text-sm font-mono bg-gray-100 px-2 py-0.5 rounded">
                    {formatValue(details.value)}
                  </span>
                </div>
                {details.metadata && (
                  <p className="text-xs text-gray-600 mt-1">
                    {formatValue(details.metadata)}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Anomaly Details */}
        <div className="bg-red-50 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-red-900">
                  {anomaly_details.type
                    .split("_")
                    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(" ")}
                </span>
                {anomaly_details.difference && (
                  <span className="text-sm font-mono bg-red-100 text-red-900 px-2 py-0.5 rounded">
                    Difference:{" "}
                    {typeof anomaly_details.difference === "number"
                      ? anomaly_details.difference.toFixed(2)
                      : formatValue(anomaly_details.difference)}
                  </span>
                )}
              </div>
              <p className="text-sm text-red-700 mt-1">
                {anomaly_details.description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAnomalies = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/anomalies");
      console.log("Raw response:", response);

      const data = await response.json();
      console.log("Parsed response data:", data);

      if (data.status === "error") {
        throw new Error(data.error);
      } else if (data.status === "empty") {
        console.log("Empty status received");
        setAnomalies(null);
      } else if (data.status === "success") {
        console.log("Setting anomalies data:", data.data);
        setAnomalies(data.data);
      } else {
        throw new Error("Invalid response format");
      }
    } catch (err) {
      console.error("Error fetching anomalies:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnomalies();
  }, []);

  return (
    <div className="h-full p-6">
      {/* Header - Always visible */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tax Anomalies</h1>
          <p className="text-gray-600 mt-1">
            Detected inconsistencies across tax documents
          </p>
        </div>
        <button
          onClick={fetchAnomalies}
          disabled={loading}
          className={`inline-flex items-center px-4 py-2 bg-red-50 text-red-700 rounded-lg transition-colors ${
            loading ? "opacity-50 cursor-not-allowed" : "hover:bg-red-100"
          }`}
        >
          <ArrowPathIcon
            className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`}
          />
          {loading ? "Analyzing..." : "Refresh Analysis"}
        </button>
      </div>

      {/* Content Area */}
      <div className="min-h-[400px] relative">
        {loading ? (
          <div className="absolute inset-0 flex items-center justify-center bg-white/80">
            <div className="text-center">
              <div className="animate-pulse flex space-x-2 justify-center mb-4">
                <div className="h-2.5 w-2.5 bg-red-400 rounded-full"></div>
                <div className="h-2.5 w-2.5 bg-red-400 rounded-full"></div>
                <div className="h-2.5 w-2.5 bg-red-400 rounded-full"></div>
              </div>
              <p className="text-sm text-gray-500">
                Analyzing tax documents...
              </p>
            </div>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center text-gray-500 py-12">
            <ExclamationTriangleIcon className="h-12 w-12 text-gray-400 mb-4" />
            <p className="text-lg font-medium">Error Loading Anomalies</p>
            <p className="text-sm mt-2">{error}</p>
          </div>
        ) : !anomalies || Object.keys(anomalies).length === 0 ? (
          <div className="flex flex-col items-center justify-center text-gray-500 py-12">
            <DocumentMagnifyingGlassIcon className="h-12 w-12 text-gray-400 mb-4" />
            <p className="text-lg font-medium">No Anomalies Found</p>
            <p className="text-sm mt-2">
              All tax documents appear to be consistent
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(anomalies).map(([key, value]) => (
              <AnomalyCard
                key={key}
                title={key
                  .split("_")
                  .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                  .join(" ")}
                data={value}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
