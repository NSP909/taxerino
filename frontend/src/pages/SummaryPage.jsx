import {
  DocumentTextIcon,
  ArrowPathIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/outline";
import { useTaxSummary } from "../hooks/useTaxSummary";
import RecommendedDocuments from "../components/Summary/RecommendedDocuments";
import { useState } from "react";

// Helper function to render nested objects
const renderNestedObject = (obj) => {
  if (!obj || typeof obj !== "object") return obj;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(obj).map(([key, value]) => (
        <div key={key} className="bg-emerald-50/50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-emerald-800 capitalize mb-2">
            {key.split("_").join(" ")}
          </h4>
          <p className="text-sm text-emerald-700 leading-relaxed">
            {typeof value === "string" ? value : renderNestedObject(value)}
          </p>
        </div>
      ))}
    </div>
  );
};

// Collapsible Section Component
const Section = ({ title, children, defaultExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className="border-b border-emerald-100 last:border-0 py-2">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between py-3 text-left hover:bg-emerald-50/50 px-4 rounded-lg transition-colors"
      >
        <h2 className="text-lg font-semibold text-emerald-900">{title}</h2>
        <ChevronDownIcon
          className={`h-5 w-5 text-emerald-600 transition-transform ${
            isExpanded ? "transform rotate-180" : ""
          }`}
        />
      </button>
      {isExpanded && <div className="px-4 pb-4 pt-2">{children}</div>}
    </div>
  );
};

export default function SummaryPage() {
  const { documentsData, taxSummary, isLoading, refreshData } = useTaxSummary();

  // Parse the JSON response from the LLM
  const parsedSummary = (() => {
    if (taxSummary?.status !== "success") return null;
    try {
      return JSON.parse(taxSummary.summary);
    } catch (error) {
      console.error("Failed to parse summary:", error);
      return null;
    }
  })();

  const hasValidSummary =
    parsedSummary?.summary && parsedSummary?.recommended_documents;

  // Define the sections to display
  const sections = [
    { id: "overview", title: "Overview", defaultExpanded: true },
    { id: "implications", title: "Tax Implications", defaultExpanded: true },
    { id: "deductions", title: "Deductions and Credits" },
    { id: "credits", title: "Available Credits" },
    { id: "deadlines", title: "Important Deadlines" },
    { id: "recommendations", title: "Recommendations", defaultExpanded: true },
    { id: "concerns", title: "Areas of Attention" },
    { id: "retirement_planning", title: "Retirement Planning" },
    { id: "investment_tax", title: "Investment Tax Analysis" },
  ];

  return (
    <div className="h-[calc(100vh-4rem)] p-4">
      <div className="flex gap-4 h-full">
        {/* Main Content */}
        <div className="flex-1">
          <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10">
            {/* Header */}
            <div className="border-b border-emerald-900/10 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-lg font-bold text-emerald-900">
                    Tax Analysis
                  </h1>
                  <p className="text-xs text-emerald-600">
                    Comprehensive analysis of your tax documents
                  </p>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="flex items-center text-xs text-emerald-600">
                    <DocumentTextIcon className="h-4 w-4 mr-1" />
                    <span>
                      {documentsData ? Object.keys(documentsData).length : 0}{" "}
                      data points
                    </span>
                  </div>
                  <button
                    onClick={refreshData}
                    disabled={isLoading}
                    className={`inline-flex items-center px-2 py-1 rounded-lg text-xs font-medium transition-colors
                      ${
                        isLoading
                          ? "bg-emerald-100 text-emerald-400 cursor-not-allowed"
                          : "bg-emerald-50 text-emerald-600 hover:bg-emerald-100"
                      }`}
                  >
                    <ArrowPathIcon
                      className={`h-3 w-3 mr-1 ${
                        isLoading ? "animate-spin" : ""
                      }`}
                    />
                    Refresh
                  </button>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="max-h-[calc(100vh-8rem)] overflow-y-auto px-4">
              {hasValidSummary ? (
                <div className="divide-y divide-emerald-100">
                  {sections.map((section) => (
                    <Section
                      key={section.id}
                      title={section.title}
                      defaultExpanded={section.defaultExpanded}
                    >
                      {renderNestedObject(parsedSummary.summary[section.id])}
                    </Section>
                  ))}
                </div>
              ) : taxSummary?.status === "empty" ? (
                <div className="text-center py-8 text-emerald-600">
                  <p className="text-sm">No tax data available yet.</p>
                  <p className="mt-1 text-xs">
                    Please upload your documents to generate a summary.
                  </p>
                </div>
              ) : taxSummary?.status === "error" || !parsedSummary ? (
                <div className="text-center py-8 text-red-600">
                  <p className="text-sm">Error generating tax summary.</p>
                  {taxSummary?.error && (
                    <p className="mt-1 text-xs">{taxSummary.error}</p>
                  )}
                </div>
              ) : (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-pulse flex space-x-2">
                    <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                    <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                    <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recommended Documents Sidebar */}
        {hasValidSummary && (
          <div className="w-80 h-full overflow-y-auto shrink-0">
            <RecommendedDocuments
              documents={parsedSummary.recommended_documents}
            />
          </div>
        )}
      </div>
    </div>
  );
}
