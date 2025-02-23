import {
  BellIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  HomeIcon,
  DocumentDuplicateIcon,
  CogIcon,
  PhoneIcon,
  ChartPieIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import { useLocation } from "react-router-dom";

const pageConfig = {
  "/dashboard": {
    icon: HomeIcon,
    title: "Welcome to Tax Daddy",
    description: "Get started by uploading your tax documents",
  },
  "/documents": {
    icon: DocumentTextIcon,
    title: "Tax Documents",
    description: "Upload and manage your tax-related documents",
  },
  "/chat": {
    icon: ChatBubbleLeftRightIcon,
    title: "Tax Assistant",
    description: "Get instant answers to your tax-related questions",
  },
  "/call": {
    icon: PhoneIcon,
    title: "Schedule a Call",
    description: "Book a consultation with our tax experts",
  },
  "/forms": {
    icon: DocumentDuplicateIcon,
    title: "Tax Forms",
    description: "Fill and manage your tax forms",
  },
  "/settings": {
    icon: CogIcon,
    title: "Settings",
    description: "Manage your account and preferences",
  },
  "/benford": {
    icon: ChartPieIcon,
    title: "Benford's Law Analysis",
    description: "Analyze numerical patterns in your financial data",
  },
  "/anomalies": {
    icon: ExclamationTriangleIcon,
    title: "Tax Anomalies",
    description: "Review detected inconsistencies in your tax documents",
  },
};

export default function TopNav() {
  const location = useLocation();
  const currentPage = pageConfig[location.pathname];

  return (
    <div className="h-24 bg-white border-b border-emerald-900/10">
      <div className="h-full px-6 flex items-center justify-between">
        {/* Page Title Section */}
        <div className="flex items-center space-x-4">
          {currentPage && (
            <>
              <div className="h-12 w-12 bg-emerald-100 rounded-lg flex items-center justify-center">
                <currentPage.icon className="h-7 w-7 text-emerald-700" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-emerald-900">
                  {currentPage.title}
                </h1>
                <p className="text-sm text-emerald-600">
                  {currentPage.description}
                </p>
              </div>
            </>
          )}
        </div>

        {/* Right Section */}
        <div className="flex items-center space-x-6">
          {/* Notifications */}
          <button className="p-2 text-emerald-600 hover:text-emerald-700 rounded-full hover:bg-emerald-50">
            <BellIcon className="h-6 w-6" />
          </button>

          {/* Profile */}
          <div className="flex items-center space-x-3">
            <div className="flex flex-col items-end">
              <span className="text-sm font-medium text-emerald-900">
                John Doe
              </span>
              <span className="text-xs text-emerald-600">john@example.com</span>
            </div>
            <button className="h-8 w-8 rounded-full bg-emerald-100 flex items-center justify-center">
              <span className="text-sm font-medium text-emerald-700">JD</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
