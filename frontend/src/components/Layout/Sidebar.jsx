import { Link, useLocation } from "react-router-dom";
import {
  HomeIcon,
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
  DocumentDuplicateIcon,
  CogIcon,
} from "@heroicons/react/24/outline";

const navItems = [
  { name: "Dashboard", icon: HomeIcon, path: "/dashboard" },
  { name: "Documents", icon: DocumentTextIcon, path: "/documents" },
  { name: "Tax Chat", icon: ChatBubbleLeftRightIcon, path: "/chat" },
  { name: "Forms", icon: DocumentDuplicateIcon, path: "/forms" },
  { name: "Settings", icon: CogIcon, path: "/settings" },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div className="h-full w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4">
        <h1 className="text-2xl font-bold text-indigo-600">Taxerino</h1>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                isActive
                  ? "bg-indigo-50 text-indigo-600"
                  : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              <item.icon className="h-5 w-5 mr-3" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
