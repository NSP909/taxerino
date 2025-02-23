import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  DocumentTextIcon,
  ArrowRightIcon,
  DocumentArrowUpIcon,
  ArrowPathIcon,
} from "@heroicons/react/24/outline";
import { AnalysisService } from "../../services/analysisService";

export default function TaxSummaryPreview() {
  const [taxSummary, setTaxSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTaxSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await AnalysisService.getTaxSummary();
      if (data?.summary && data?.status === "success") {
        // Parse the stringified JSON summary
        try {
          const parsedSummary = JSON.parse(data.summary);
          setTaxSummary(parsedSummary);
        } catch (parseError) {
          console.error("Failed to parse summary:", parseError);
          setError("Invalid summary format");
        }
      } else {
        setTaxSummary(null);
      }
    } catch (error) {
      console.error("Failed to fetch tax summary:", error);
      setError("Failed to load tax summary");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTaxSummary();
  }, []);

  const getPreviewData = (summary) => {
    try {
      return {
        income: summary.overview.total_income,
        status: summary.overview.filing_status,
        nextDeadline: summary.deadlines.filing_deadline,
        keyAction: summary.recommendations.immediate_actions,
      };
    } catch (error) {
      console.error("Failed to parse summary:", error);
      return null;
    }
  };

  const previewData = taxSummary ? getPreviewData(taxSummary.summary) : null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10 p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-emerald-900">
            Tax Summary
          </h2>
          <p className="text-sm text-emerald-600">
            Quick overview of your tax analysis
          </p>
        </div>
        <button
          onClick={fetchTaxSummary}
          disabled={loading}
          className="text-emerald-600 hover:text-emerald-700"
        >
          <ArrowPathIcon
            className={`h-5 w-5 ${loading ? "animate-spin" : ""}`}
          />
        </button>
      </div>

      {error ? (
        <div className="text-center py-6">
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchTaxSummary}
            className="mt-2 text-sm text-emerald-600 hover:text-emerald-700"
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
      ) : previewData ? (
        <>
          <div className="space-y-4 mb-4">
            {/* Key Information Grid */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-emerald-50/50 rounded-lg p-4">
                <h3 className="text-xs font-medium text-emerald-800 uppercase tracking-wide mb-1">
                  Total Income
                </h3>
                <p className="text-sm text-emerald-900">{previewData.income}</p>
              </div>
              <div className="bg-emerald-50/50 rounded-lg p-4">
                <h3 className="text-xs font-medium text-emerald-800 uppercase tracking-wide mb-1">
                  Filing Status
                </h3>
                <p className="text-sm text-emerald-900">{previewData.status}</p>
              </div>
            </div>

            {/* Next Deadline */}
            <div className="bg-emerald-50/50 rounded-lg p-4">
              <h3 className="text-xs font-medium text-emerald-800 uppercase tracking-wide mb-1">
                Next Deadline
              </h3>
              <p className="text-sm text-emerald-900">
                {previewData.nextDeadline}
              </p>
            </div>

            {/* Recommended Action */}
            <div className="bg-emerald-50/50 rounded-lg p-4">
              <h3 className="text-xs font-medium text-emerald-800 uppercase tracking-wide mb-1">
                Recommended Action
              </h3>
              <p className="text-sm text-emerald-900">
                {previewData.keyAction}
              </p>
            </div>
          </div>
          <Link
            to="/summary"
            className="inline-flex items-center text-sm text-emerald-600 hover:text-emerald-700 font-medium"
          >
            View full analysis
            <ArrowRightIcon className="h-4 w-4 ml-1" />
          </Link>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center py-8 px-4">
          <DocumentArrowUpIcon className="h-12 w-12 text-emerald-200 mb-4" />
          <p className="text-emerald-900 font-medium text-center mb-2">
            No tax analysis available yet
          </p>
          <p className="text-emerald-600 text-sm text-center mb-6">
            Upload your tax documents to get a comprehensive analysis of your
            tax situation
          </p>
          <Link
            to="/documents"
            className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Upload Documents
            <ArrowRightIcon className="h-4 w-4 ml-2" />
          </Link>
        </div>
      )}
    </div>
  );
}
