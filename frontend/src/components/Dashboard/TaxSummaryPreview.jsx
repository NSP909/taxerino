import { Link } from "react-router-dom";
import {
  DocumentTextIcon,
  ArrowRightIcon,
  DocumentArrowUpIcon,
  ArrowPathIcon,
} from "@heroicons/react/24/outline";

export default function TaxSummaryPreview({
  taxSummary,
  documentsData,
  generateTaxSummary,
  isLoading,
}) {
  const getPreviewData = (summary) => {
    try {
      const data = JSON.parse(summary);
      return {
        income: data.summary.overview.total_income,
        status: data.summary.overview.filing_status,
        nextDeadline: data.summary.deadlines.filing_deadline,
        keyAction: data.summary.recommendations.immediate_actions,
      };
    } catch (error) {
      console.error("Failed to parse summary:", error);
      return null;
    }
  };

  const previewData =
    taxSummary?.status === "success"
      ? getPreviewData(taxSummary.summary)
      : null;
  const hasDocuments = documentsData && Object.keys(documentsData).length > 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10 p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-emerald-900">
            Tax Summary
          </h2>
          <p className="text-sm text-emerald-600">
            {hasDocuments
              ? "Quick overview of your tax analysis"
              : "Upload documents to get your tax analysis"}
          </p>
        </div>
        <div className="flex items-center text-sm text-emerald-600">
          <DocumentTextIcon className="h-5 w-5 mr-2" />
          <span>
            {documentsData ? Object.keys(documentsData).length : 0} data points
          </span>
        </div>
      </div>

      {taxSummary?.status === "success" && previewData ? (
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
      ) : hasDocuments && !isLoading ? (
        <div className="flex flex-col items-center justify-center py-8 px-4">
          <DocumentTextIcon className="h-12 w-12 text-emerald-200 mb-4" />
          <p className="text-emerald-900 font-medium text-center mb-2">
            Documents uploaded successfully
          </p>
          <p className="text-emerald-600 text-sm text-center mb-6">
            Generate a tax analysis to get insights about your tax situation
          </p>
          <button
            onClick={generateTaxSummary}
            className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Generate Analysis
            <ArrowPathIcon
              className={`h-4 w-4 ml-2 ${isLoading ? "animate-spin" : ""}`}
            />
          </button>
        </div>
      ) : isLoading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-pulse flex space-x-2">
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
          </div>
        </div>
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
