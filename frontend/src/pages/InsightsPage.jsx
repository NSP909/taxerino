import { useState, useEffect } from "react";
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
import { AnalysisService } from "../services/analysisService";

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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisData, setAnalysisData] = useState({
    taxSummary: null,
    taxPlots: null,
    benford: null,
    anomalies: null,
  });

  useEffect(() => {
    fetchAnalysisData();
  }, []);

  const fetchAnalysisData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [taxSummary, taxPlots, benford, anomalies] = await Promise.all([
        AnalysisService.getTaxSummary(),
        AnalysisService.getTaxPlots(),
        AnalysisService.getBenfordAnalysis(),
        AnalysisService.getAnomalies(),
      ]);

      // Parse the nested JSON string in taxSummary
      let parsedTaxSummary = null;
      if (taxSummary?.status === "success" && taxSummary?.summary) {
        try {
          parsedTaxSummary = JSON.parse(taxSummary.summary);
        } catch (e) {
          console.error("Failed to parse tax summary:", e);
        }
      }

      setAnalysisData({
        taxSummary: parsedTaxSummary,
        taxPlots,
        benford,
        anomalies,
      });
    } catch (error) {
      console.error("Failed to fetch analysis data:", error);
      setError("Failed to load analysis data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const renderSectionContent = (section) => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-8">
          <div className="animate-pulse flex space-x-2">
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
            <div className="h-2 w-2 bg-emerald-400 rounded-full"></div>
          </div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="text-center py-10">
          <ExclamationCircleIcon className="h-14 w-14 text-red-200 mx-auto mb-4" />
          <p className="text-lg text-red-900 font-medium">{error}</p>
        </div>
      );
    }

    if (!analysisData.taxSummary && section !== "visualizations") {
      return (
        <div className="text-center py-10">
          <ExclamationCircleIcon className="h-14 w-14 text-emerald-200 mx-auto mb-4" />
          <p className="text-lg text-emerald-900 font-medium">
            No tax summary available
          </p>
          <p className="text-base text-emerald-600 mt-2">
            Upload tax documents to view analysis
          </p>
        </div>
      );
    }

    const summary = analysisData.taxSummary?.summary;

    switch (section) {
      case "overview":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">Overview</h2>
            <div className="grid grid-cols-1 gap-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Total Income
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.overview.total_income}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Filing Status
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.overview.filing_status}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Tax Bracket
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.overview.tax_bracket}
                </p>
              </div>
            </div>
          </div>
        );

      case "implications":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Tax Implications
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Tax Liability
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.implications.tax_liability}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Marginal Rate
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.implications.marginal_rate}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  State Tax Impact
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.implications.state_tax_impact}
                </p>
              </div>
            </div>
          </div>
        );

      case "deductions":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">Deductions</h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Standard vs Itemized
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deductions.standard_vs_itemized}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Available Deductions
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deductions.available_deductions}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Estimated Savings
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deductions.estimated_savings}
                </p>
              </div>
            </div>
          </div>
        );

      case "credits":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">Tax Credits</h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Eligible Credits
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.credits.eligible_credits}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Requirements
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.credits.requirements}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Estimated Benefit
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.credits.estimated_benefit}
                </p>
              </div>
            </div>
          </div>
        );

      case "deadlines":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Important Deadlines
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Filing Deadline
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deadlines.filing_deadline}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Estimated Tax
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deadlines.estimated_tax}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Extension Options
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.deadlines.extension_options}
                </p>
              </div>
            </div>
          </div>
        );

      case "recommendations":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Recommendations
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Immediate Actions
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.recommendations.immediate_actions}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Tax Planning
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.recommendations.tax_planning}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Savings Opportunities
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.recommendations.savings_opportunities}
                </p>
              </div>
            </div>
          </div>
        );

      case "concerns":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Areas of Attention
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Risk Areas
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.concerns.risk_areas}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Missing Information
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.concerns.missing_information}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Compliance Issues
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.concerns.compliance_issues}
                </p>
              </div>
            </div>
          </div>
        );

      case "retirement_planning":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Retirement Planning
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Contribution Limits
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.retirement_planning.contribution_limits}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Tax Advantages
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.retirement_planning.tax_advantages}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Recommendations
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.retirement_planning.recommendations}
                </p>
              </div>
            </div>
          </div>
        );

      case "investment_tax":
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Investment Tax Analysis
            </h2>
            <div className="space-y-4">
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Capital Gains
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.investment_tax.capital_gains}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Loss Harvesting
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.investment_tax.loss_harvesting}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-emerald-900">
                  Investment Strategies
                </h3>
                <p className="mt-2 text-sm text-emerald-700">
                  {summary.investment_tax.investment_strategies}
                </p>
              </div>
            </div>
          </div>
        );

      case "visualizations":
        return analysisData.taxPlots ? (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-emerald-900">
              Tax Data Visualizations
            </h2>

            <div className="space-y-8">
              {/* Sort and group visualizations by type */}
              {(() => {
                const plots = analysisData.taxPlots;
                const pieCharts = [];
                const barCharts = [];
                const scatterPlots = [];
                const heatmaps = [];
                const lineCharts = [];

                // Group charts by type
                Object.entries(plots).forEach(([key, value]) => {
                  const chartInfo = value[Object.keys(value)[0]];
                  const chartType = chartInfo.type
                    .toLowerCase()
                    .replace(/\s+/g, "");
                  const chartComponent = (
                    <div
                      key={key}
                      className="bg-emerald-50 rounded-lg p-6 flex flex-col shadow-sm hover:shadow-md transition-shadow"
                    >
                      <h3 className="text-lg font-medium text-emerald-900">
                        {chartInfo.parameters.title}
                      </h3>
                      <p className="text-sm text-emerald-600 mt-2 mb-4">
                        {chartInfo.description}
                      </p>
                      <div className="bg-white rounded-lg p-4 flex-1 h-[400px]">
                        <FinancialCharts
                          data={{
                            [key]: value,
                          }}
                        />
                      </div>
                    </div>
                  );

                  switch (chartType) {
                    case "piechart":
                      pieCharts.push(chartComponent);
                      break;
                    case "barchart":
                      barCharts.push(chartComponent);
                      break;
                    case "scatterplot":
                      scatterPlots.push(chartComponent);
                      break;
                    case "heatmap":
                      heatmaps.push(chartComponent);
                      break;
                    case "linechart":
                      lineCharts.push(chartComponent);
                      break;
                  }
                });

                return (
                  <>
                    {/* Pie Charts in a grid */}
                    {pieCharts.length > 0 && (
                      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                        {pieCharts}
                      </div>
                    )}

                    {/* Other chart types in sequence */}
                    {barCharts.length > 0 && (
                      <div className="space-y-6">{barCharts}</div>
                    )}
                    {scatterPlots.length > 0 && (
                      <div className="space-y-6">{scatterPlots}</div>
                    )}
                    {heatmaps.length > 0 && (
                      <div className="space-y-6">{heatmaps}</div>
                    )}
                    {lineCharts.length > 0 && (
                      <div className="space-y-6">{lineCharts}</div>
                    )}
                  </>
                );
              })()}
            </div>
          </div>
        ) : (
          <div className="text-center py-10">
            <ExclamationCircleIcon className="h-14 w-14 text-emerald-200 mx-auto mb-4" />
            <p className="text-lg text-emerald-900 font-medium">
              No visualization data available
            </p>
            <p className="text-base text-emerald-600 mt-2">
              Upload tax documents to view visualizations
            </p>
          </div>
        );

      default:
        return null;
    }
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
          onClick={fetchAnalysisData}
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
            {renderSectionContent(selectedSection)}
          </div>
        </div>
      </div>
    </div>
  );
}
