import { useState } from "react";
import { useTaxSummary } from "../hooks/useTaxSummary";
import { useTaxPlots } from "../hooks/useTaxPlots";
import {
  ChartBarIcon,
  ArrowPathIcon,
  ExclamationCircleIcon,
  DocumentChartBarIcon,
  CurrencyDollarIcon,
  CalculatorIcon,
  ClockIcon,
  LightBulbIcon,
  ExclamationTriangleIcon,
  BanknotesIcon,
  PresentationChartLineIcon,
} from "@heroicons/react/24/outline";
import FinancialCharts from "../components/Insights/FinancialCharts";

const SECTIONS = [
  {
    id: "overview",
    name: "Overview",
    description: "Key tax metrics and status",
    icon: DocumentChartBarIcon,
  },
  {
    id: "implications",
    name: "Tax Implications",
    description: "Understanding your tax obligations",
    icon: CurrencyDollarIcon,
  },
  {
    id: "deductions",
    name: "Deductions and Credits",
    description: "Available tax deductions and savings",
    icon: CalculatorIcon,
  },
  {
    id: "credits",
    name: "Available Credits",
    description: "Tax credits you can claim",
    icon: BanknotesIcon,
  },
  {
    id: "deadlines",
    name: "Important Deadlines",
    description: "Key dates and deadlines",
    icon: ClockIcon,
  },
  {
    id: "recommendations",
    name: "Recommendations",
    description: "Suggested tax optimization steps",
    icon: LightBulbIcon,
  },
  {
    id: "concerns",
    name: "Areas of Attention",
    description: "Points requiring attention",
    icon: ExclamationTriangleIcon,
  },
  {
    id: "retirement_planning",
    name: "Retirement Planning",
    description: "Tax-efficient retirement strategies",
    icon: PresentationChartLineIcon,
  },
  {
    id: "investment_tax",
    name: "Investment Tax Analysis",
    description: "Investment tax implications",
    icon: ChartBarIcon,
  },
  {
    id: "visualizations",
    name: "Visualizations",
    description: "Tax data visualizations",
    icon: ChartBarIcon,
  },
];

export default function InsightsPage() {
  const {
    documentsData,
    taxSummary,
    isLoading: summaryLoading,
    refreshData,
  } = useTaxSummary();
  const {
    plotData,
    isLoading: plotsLoading,
    error: plotError,
    refreshPlotData,
  } = useTaxPlots();
  const [selectedSection, setSelectedSection] = useState("overview");

  const getInsightData = (summary) => {
    try {
      const data = JSON.parse(summary);
      return data.summary;
    } catch (error) {
      console.error("Failed to parse summary:", error);
      return null;
    }
  };

  const insightData =
    taxSummary?.status === "success"
      ? getInsightData(taxSummary.summary)
      : null;

  const handleRefresh = async () => {
    try {
      const refreshPromises = [refreshData(true), refreshPlotData(true)];
      await Promise.all(refreshPromises);
    } catch (error) {
      console.error("Error refreshing data:", error);
    }
  };

  const renderSectionContent = (section) => {
    if (section === "visualizations") {
      return (
        <div>
          <h2 className="text-xl font-bold text-emerald-900 mb-5">
            Tax Data Visualizations
          </h2>
          {plotError ? (
            <div className="text-center py-10">
              <ExclamationCircleIcon className="h-14 w-14 text-red-200 mx-auto mb-4" />
              <p className="text-lg text-red-900 font-medium">
                Error Loading Visualizations
              </p>
              <p className="text-base text-red-600 mt-2">{plotError}</p>
            </div>
          ) : plotsLoading ? (
            <div className="flex items-center justify-center py-10">
              <div className="animate-pulse flex space-x-2">
                <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
                <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
                <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
              </div>
            </div>
          ) : plotData ? (
            <FinancialCharts data={plotData} />
          ) : (
            <div className="text-center py-10">
              <ChartBarIcon className="h-14 w-14 text-emerald-200 mx-auto mb-4" />
              <p className="text-lg text-emerald-900 font-medium">
                Click Refresh Analysis to View Visualizations
              </p>
              <p className="text-base text-emerald-600 mt-2">
                The visualizations will be generated based on your tax data
              </p>
            </div>
          )}
        </div>
      );
    }

    if (summaryLoading) {
      return (
        <div className="flex items-center justify-center py-10">
          <div className="animate-pulse flex space-x-2">
            <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
            <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
            <div className="h-2.5 w-2.5 bg-emerald-400 rounded-full"></div>
          </div>
        </div>
      );
    }

    if (!insightData || !insightData[section]) {
      return (
        <div className="text-center py-10">
          <ExclamationCircleIcon className="h-14 w-14 text-emerald-200 mx-auto mb-4" />
          <p className="text-lg text-emerald-900 font-medium">
            No Data Available
          </p>
          <p className="text-base text-emerald-600 mt-2">
            Click Refresh Analysis to view this section
          </p>
        </div>
      );
    }

    return (
      <div>
        <h2 className="text-xl font-bold text-emerald-900 mb-5">
          {SECTIONS.find((s) => s.id === section)?.name}
        </h2>
        <div className="space-y-4">
          {Object.entries(insightData[section]).map(([key, value]) => (
            <div
              key={key}
              className="bg-emerald-50/50 rounded-lg p-5 border border-emerald-100 hover:shadow-md transition-shadow"
            >
              <h3 className="text-base font-semibold text-emerald-800 capitalize mb-2">
                {key.split("_").join(" ")}
              </h3>
              <p className="text-sm text-emerald-700 leading-relaxed">
                {value}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="h-full p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">Tax Insights</h1>
          <p className="text-base text-emerald-600 mt-1">
            AI-powered analysis of your tax situation
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={summaryLoading && plotsLoading}
          className={`inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${
              summaryLoading && plotsLoading
                ? "bg-emerald-100 text-emerald-400 cursor-not-allowed"
                : "bg-emerald-50 text-emerald-600 hover:bg-emerald-100"
            }`}
        >
          <ArrowPathIcon
            className={`h-4 w-4 mr-2 ${
              summaryLoading || plotsLoading ? "animate-spin" : ""
            }`}
          />
          {summaryLoading && plotsLoading
            ? "Refreshing..."
            : "Refresh Analysis"}
          {(summaryLoading || plotsLoading) &&
            !(summaryLoading && plotsLoading) && (
              <span className="ml-2 text-xs">
                {summaryLoading ? "Loading Summary..." : "Loading Plots..."}
              </span>
            )}
        </button>
      </div>

      <div className="flex gap-6">
        {/* Navigation Sidebar */}
        <div className="w-72 shrink-0">
          <div className="bg-white rounded-lg shadow-sm border border-emerald-900/10 p-3">
            <nav className="space-y-1">
              {SECTIONS.map((section) => {
                const Icon = section.icon;
                return (
                  <button
                    key={section.id}
                    onClick={() => setSelectedSection(section.id)}
                    className={`w-full text-left px-3 py-2.5 rounded-lg transition-colors flex items-center ${
                      selectedSection === section.id
                        ? "bg-emerald-50 text-emerald-900"
                        : "text-emerald-600 hover:bg-emerald-50/50"
                    }`}
                  >
                    <Icon className="h-5 w-5 mr-3 flex-shrink-0" />
                    <div>
                      <span className="text-sm font-medium block">
                        {section.name}
                      </span>
                      <span className="text-xs text-emerald-500 block mt-0.5">
                        {section.description}
                      </span>
                    </div>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <div className="bg-white rounded-lg shadow-sm border border-emerald-900/10 p-6">
            {!documentsData || Object.keys(documentsData).length === 0 ? (
              <div className="text-center py-10">
                <ExclamationCircleIcon className="h-14 w-14 text-emerald-200 mx-auto mb-4" />
                <p className="text-lg text-emerald-900 font-medium">
                  No Documents Found
                </p>
                <p className="text-base text-emerald-600 mt-2">
                  Upload your tax documents to get insights
                </p>
              </div>
            ) : (
              renderSectionContent(selectedSection)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
