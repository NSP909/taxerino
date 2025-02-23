import { Link } from "react-router-dom";
import {
  DocumentTextIcon,
  PhoneIcon,
  ChartBarIcon,
  DocumentChartBarIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

const steps = [
  {
    id: 1,
    name: "Documents Upload",
    description: "Upload your tax documents",
    icon: DocumentTextIcon,
    path: "/documents",
  },
  {
    id: 2,
    name: "Schedule Call",
    description: "Book a consultation",
    icon: PhoneIcon,
    path: "/call",
  },
  {
    id: 3,
    name: "View Insights",
    description: "AI-powered tax insights",
    icon: ChartBarIcon,
    path: "/insights",
  },
  {
    id: 4,
    name: "Tax Summary",
    description: "Complete tax analysis",
    icon: DocumentChartBarIcon,
    path: "/summary",
  },
  {
    id: 5,
    name: "Complete",
    description: "All steps completed",
    icon: CheckCircleIcon,
    path: null,
  },
];

export default function ProgressTracker({
  documentsUploaded = false,
  currentStep = 1,
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-emerald-900/10 p-6 w-full">
      <h2 className="text-lg font-semibold text-emerald-900 mb-6">
        Tax Progress
      </h2>

      <div className="relative">
        {/* Progress Line */}
        <div className="absolute top-5 left-5 right-5 h-0.5 bg-emerald-100">
          <div
            className="absolute top-0 left-0 h-full bg-emerald-600 transition-all duration-500"
            style={{
              width: `${((currentStep - 1) / (steps.length - 1)) * 100}%`,
            }}
          />
        </div>

        {/* Steps */}
        <div className="relative flex justify-between">
          {steps.map((step) => {
            const isCompleted = step.id < currentStep;
            const isCurrent = step.id === currentStep;

            return (
              <div key={step.id} className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors ${
                    isCompleted
                      ? "bg-emerald-600 border-emerald-600"
                      : isCurrent
                      ? "bg-white border-emerald-600"
                      : "bg-white border-emerald-200"
                  }`}
                >
                  <step.icon
                    className={`w-5 h-5 ${
                      isCompleted
                        ? "text-white"
                        : isCurrent
                        ? "text-emerald-600"
                        : "text-emerald-200"
                    }`}
                  />
                </div>
                <div className="flex flex-col items-center mt-2">
                  <span
                    className={`text-sm font-medium ${
                      isCompleted || isCurrent
                        ? "text-emerald-900"
                        : "text-emerald-300"
                    }`}
                  >
                    {step.name}
                  </span>
                  <span
                    className={`text-xs mt-0.5 ${
                      isCompleted || isCurrent
                        ? "text-emerald-600"
                        : "text-emerald-300"
                    }`}
                  >
                    {step.description}
                  </span>
                  {step.id === 1 && !documentsUploaded && (
                    <span className="text-xs font-medium text-red-500 mt-1">
                      Not Started
                    </span>
                  )}
                  {isCompleted && (
                    <span className="text-xs font-medium text-emerald-600 mt-1">
                      Completed
                    </span>
                  )}
                  {isCurrent && (
                    <span className="text-xs font-medium text-emerald-600 mt-1">
                      In Progress
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Button */}
      <div className="mt-8 flex justify-center">
        {!documentsUploaded && currentStep === 1 && (
          <Link
            to="/documents"
            className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            <DocumentTextIcon className="w-5 h-5 mr-2" />
            Upload Documents
          </Link>
        )}
        {documentsUploaded && currentStep === 2 && (
          <Link
            to="/call"
            className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            <PhoneIcon className="w-5 h-5 mr-2" />
            Schedule Call
          </Link>
        )}
        {currentStep === 3 && (
          <Link
            to="/insights"
            className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            <ChartBarIcon className="w-5 h-5 mr-2" />
            View Insights
          </Link>
        )}
      </div>
    </div>
  );
}
