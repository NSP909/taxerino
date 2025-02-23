import { Link } from "react-router-dom";
import {
  DocumentArrowUpIcon,
  ArrowRightIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";

export default function RecommendedDocuments({ documents = [] }) {
  // Sort documents by priority
  const sortedDocs = [...documents].sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  return (
    <div className="w-80 bg-white rounded-xl shadow-sm border border-emerald-900/10 h-fit">
      <div className="p-6 border-b border-emerald-900/10">
        <h3 className="text-lg font-semibold text-emerald-900">
          Recommended Documents
        </h3>
        <p className="text-sm text-emerald-600 mt-1">
          Additional documents needed for a complete analysis
        </p>
      </div>

      <div className="p-4 space-y-4">
        {sortedDocs.length > 0 ? (
          sortedDocs.map((doc) => (
            <div
              key={doc.type}
              className="bg-emerald-50 rounded-lg p-4 space-y-3"
            >
              <div className="flex items-start">
                <DocumentArrowUpIcon className="h-5 w-5 text-emerald-600 mr-3 flex-shrink-0 mt-0.5" />
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-medium text-emerald-900">
                      {doc.name}
                    </h4>
                    {doc.priority === "high" && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                        <ExclamationCircleIcon className="w-3 h-3 mr-1" />
                        High Priority
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-emerald-600 mt-1">
                    {doc.description}
                  </p>
                </div>
              </div>
              <Link
                to="/documents"
                className="block text-center px-3 py-2 bg-emerald-100 text-sm font-medium text-emerald-700 rounded-lg hover:bg-emerald-200 transition-colors"
              >
                Upload Document
                <ArrowRightIcon className="inline-block h-4 w-4 ml-1.5 -mt-0.5" />
              </Link>
            </div>
          ))
        ) : (
          <div className="text-center py-6 text-emerald-600">
            <p className="text-sm">No additional documents needed</p>
          </div>
        )}
      </div>
    </div>
  );
}
