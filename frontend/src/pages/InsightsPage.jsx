import { useState } from "react";
import { useTaxSummary } from "../hooks/useTaxSummary";
import {
  ChartBarIcon,
  ArrowPathIcon,
  ExclamationCircleIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

export default function InsightsPage() {
  const { documentsData, taxSummary, isLoading, refreshData } = useTaxSummary();
  const [selectedSection, setSelectedSection] = useState("overview");

  const getInsightData = (summary) => {
    try {
      const data = JSON.parse(summary);
      return {
        overview: data.summary.overview,
        implications: data.summary.implications,
        deductions: data.summary.deductions,
        retirement: data.summary.retirement_planning,
        investment: data.summary.investment_tax,
      };
    } catch (error) {
      console.error("Failed to parse summary:", error);
      return null;
    }
  };

  const insightData =
    taxSummary?.status === "success"
      ? getInsightData(taxSummary.summary)
      : null;

  const sections = [
    {
      id: "overview",
      name: "Overview",
      description: "Key tax metrics and status",
    },
    {
      id: "implications",
      name: "Tax Implications",
      description: "Understanding your tax obligations",
    },
    {
      id: "deductions",
      name: "Deductions",
      description: "Available tax deductions and savings",
    },
    {
      id: "retirement",
      name: "Retirement Planning",
      description: "Tax-efficient retirement strategies",
    },
    {
      id: "investment",
      name: "Investment Analysis",
      description: "Investment tax implications",
    },
  ];

  return (
    <div className="h-full p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">Tax Insights</h1>
          <p className="text-emerald-600 mt-1">
            AI-powered analysis of your tax situation
          </p>
        </div>
        <button
          onClick={() => refreshData(true)}
          disabled={isLoading}
          className={`inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors
            ${
              isLoading
                ? "bg-emerald-100 text-emerald-400 cursor-not-allowed"
                : "bg-emerald-50 text-emerald-600 hover:bg-emerald-100"
            }`}
        >
          <ArrowPathIcon
            className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`}
          />
          Refresh Analysis
        </button>
      </div>

      <div className="flex gap-6">
        {/* Navigation Sidebar */}
        <div className="w-64 shrink-0">
          <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10 p-4">
            <nav className="space-y-1">
              {sections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setSelectedSection(section.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                    selectedSection === section.id
                      ? "bg-emerald-50 text-emerald-900"
                      : "text-emerald-600 hover:bg-emerald-50/50"
                  }`}
                >
                  <span className="text-sm font-medium">{section.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10 p-6">
            {!documentsData || Object.keys(documentsData).length === 0 ? (
              <div className="text-center py-8">
                <ExclamationCircleIcon className="h-12 w-12 text-emerald-200 mx-auto mb-4" />
                <p className="text-emerald-900 font-medium">
                  No Documents Found
                </p>
                <p className="text-emerald-600 text-sm mt-1">
                  Upload your tax documents to get insights
                </p>
              </div>
            ) : isLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-pulse flex space-x-2">
                  <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                  <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                  <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
                </div>
              </div>
            ) : insightData ? (
              <div>
                <h2 className="text-lg font-semibold text-emerald-900 mb-4">
                  {sections.find((s) => s.id === selectedSection)?.name}
                </h2>
                <div className="space-y-4">
                  {Object.entries(insightData[selectedSection] || {}).map(
                    ([key, value]) => (
                      <div
                        key={key}
                        className="bg-emerald-50/50 rounded-lg p-4"
                      >
                        <h3 className="text-sm font-medium text-emerald-800 capitalize mb-2">
                          {key.split("_").join(" ")}
                        </h3>
                        <p className="text-sm text-emerald-700">{value}</p>
                      </div>
                    )
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <ChartBarIcon className="h-12 w-12 text-emerald-200 mx-auto mb-4" />
                <p className="text-emerald-900 font-medium">
                  No Insights Available
                </p>
                <p className="text-emerald-600 text-sm mt-1">
                  Generate a tax analysis to see insights
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
