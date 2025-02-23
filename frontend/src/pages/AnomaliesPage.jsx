import { useState, useEffect } from "react";
import { AnalysisService } from "../services/analysisService";
import {
  ArrowPathIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ShieldExclamationIcon,
  BanknotesIcon,
  CalendarIcon,
} from "@heroicons/react/24/outline";

export default function AnomaliesPage() {
  const [anomaliesData, setAnomaliesData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAnomaliesData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await AnalysisService.getAnomalies();
      setAnomaliesData(data);
    } catch (error) {
      console.error("Failed to fetch anomalies:", error);
      setError("Failed to load anomalies");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnomaliesData();
  }, []);

  const getAnomalyTypeColor = (type) => {
    switch (type.toLowerCase()) {
      case "future_date":
        return {
          bg: "bg-blue-50",
          text: "text-blue-700",
          icon: "text-blue-600",
          border: "border-blue-200",
        };
      case "disproportionate_tax":
        return {
          bg: "bg-red-50",
          text: "text-red-700",
          icon: "text-red-600",
          border: "border-red-200",
        };
      case "incorrect_tax_rate":
        return {
          bg: "bg-purple-50",
          text: "text-purple-700",
          icon: "text-purple-600",
          border: "border-purple-200",
        };
      case "inconsistent_amounts":
        return {
          bg: "bg-yellow-50",
          text: "text-yellow-700",
          icon: "text-yellow-600",
          border: "border-yellow-200",
        };
      case "unusually_low":
        return {
          bg: "bg-orange-50",
          text: "text-orange-700",
          icon: "text-orange-600",
          border: "border-orange-200",
        };
      default:
        return {
          bg: "bg-emerald-50",
          text: "text-emerald-700",
          icon: "text-emerald-600",
          border: "border-emerald-200",
        };
    }
  };

  const getAnomalyIcon = (type) => {
    switch (type.toLowerCase()) {
      case "future_date":
        return CalendarIcon;
      case "disproportionate_tax":
        return ShieldExclamationIcon;
      case "incorrect_tax_rate":
        return ExclamationTriangleIcon;
      case "inconsistent_amounts":
        return BanknotesIcon;
      case "unusually_low":
        return ExclamationCircleIcon;
      default:
        return CheckCircleIcon;
    }
  };

  const formatAnomalyType = (type) => {
    return type
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="h-full p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">
            Anomaly Detection
          </h1>
          <p className="text-base text-emerald-600 mt-1">
            AI-powered detection of unusual patterns in your tax data
          </p>
        </div>
        <button
          onClick={fetchAnomaliesData}
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

      <div className="bg-white rounded-xl shadow-lg border border-emerald-900/10 p-6">
        {error ? (
          <div className="text-center py-8">
            <ExclamationCircleIcon className="h-14 w-14 text-red-200 mx-auto mb-3" />
            <p className="text-lg text-red-900 font-medium">{error}</p>
            <button
              onClick={fetchAnomaliesData}
              className="mt-3 text-sm text-emerald-600 hover:text-emerald-700"
            >
              Try again
            </button>
          </div>
        ) : loading ? (
          <div className="flex items-center justify-center py-6">
            <div className="animate-pulse flex space-x-2">
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
              <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            </div>
          </div>
        ) : anomaliesData?.anomalies?.length > 0 ? (
          <div className="space-y-4">
            <div className="grid gap-4">
              {anomaliesData.anomalies.map((anomaly, index) => {
                const Icon = getAnomalyIcon(anomaly.anomaly_type);
                const colors = getAnomalyTypeColor(anomaly.anomaly_type);
                return (
                  <div
                    key={index}
                    className={`rounded-lg border ${colors.border} ${colors.bg} p-4 transition-all duration-200 hover:shadow-md`}
                  >
                    <div className="flex items-start space-x-4">
                      <div className={`${colors.bg} rounded-md p-2`}>
                        <Icon className={`h-6 w-6 ${colors.icon}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div>
                            <h3
                              className={`text-base font-semibold ${colors.text}`}
                            >
                              {formatAnomalyType(anomaly.anomaly_type)}
                            </h3>
                            <p
                              className={`text-xs mt-0.5 ${colors.text} opacity-75`}
                            >
                              Field: {anomaly.field}
                            </p>
                          </div>
                        </div>
                        <p className={`mt-2 text-sm ${colors.text}`}>
                          {anomaly.description}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <CheckCircleIcon className="h-14 w-14 text-emerald-200 mx-auto mb-3" />
            <p className="text-lg text-emerald-900 font-medium">
              No anomalies detected
            </p>
            <p className="text-base text-emerald-600 mt-2">
              Your tax data appears to be consistent
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
