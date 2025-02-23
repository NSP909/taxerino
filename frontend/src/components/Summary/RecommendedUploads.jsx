import { useState } from "react";
import { Link } from "react-router-dom";
import {
  DocumentArrowUpIcon,
  ArrowRightIcon,
} from "@heroicons/react/24/outline";

const RECOMMENDED_DOCS = [
  {
    id: "payslips",
    name: "Payslips",
    description: "Monthly or periodic payment records",
  },
  { id: "p60", name: "P60", description: "End of year tax summary" },
  {
    id: "income",
    name: "Other Income",
    description: "Documentation of additional income sources",
  },
  {
    id: "expenses",
    name: "Expenses",
    description: "Records of tax-deductible expenses",
  },
];

export default function RecommendedUploads() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="mt-8 border-t border-emerald-900/10 pt-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-emerald-900">
            Recommended Documents
          </h3>
          <p className="text-sm text-emerald-600 mt-1">
            Upload these additional documents for a more comprehensive analysis
          </p>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-sm text-emerald-600 hover:text-emerald-700"
        >
          {isExpanded ? "Show less" : "Show all"}
        </button>
      </div>

      {isExpanded ? (
        <div className="mt-4 space-y-4">
          {RECOMMENDED_DOCS.map((doc) => (
            <div
              key={doc.id}
              className="bg-emerald-50 rounded-lg p-4 flex items-center justify-between"
            >
              <div className="flex items-center">
                <DocumentArrowUpIcon className="h-5 w-5 text-emerald-600 mr-3" />
                <div>
                  <h4 className="text-sm font-medium text-emerald-900">
                    {doc.name}
                  </h4>
                  <p className="text-xs text-emerald-600 mt-0.5">
                    {doc.description}
                  </p>
                </div>
              </div>
              <Link
                to="/documents"
                className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-emerald-600 hover:text-emerald-700"
              >
                Upload
                <ArrowRightIcon className="h-4 w-4 ml-1.5" />
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <Link
          to="/documents"
          className="mt-4 flex items-center justify-center px-4 py-3 bg-emerald-50 rounded-lg text-emerald-600 hover:text-emerald-700 hover:bg-emerald-100 transition-colors"
        >
          <DocumentArrowUpIcon className="h-5 w-5 mr-2" />
          <span className="font-medium">Upload Additional Documents</span>
          <ArrowRightIcon className="h-4 w-4 ml-2" />
        </Link>
      )}
    </div>
  );
}
