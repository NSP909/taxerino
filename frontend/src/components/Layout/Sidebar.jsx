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
    <div className="h-full w-64 bg-emerald-900 flex flex-col">
      <div className="p-4">
        <Link to="/" className="flex items-center group">
          <div className="h-10 w-10 rounded-xl bg-emerald-600/20 border border-emerald-500/20 flex items-center justify-center group-hover:border-emerald-500/40 transition-colors">
            <div className="h-6 w-6 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/50 group-hover:shadow-emerald-500/70"></div>
          </div>
          <span className="ml-3 text-xl text-white font-medium tracking-wide">
            Taxerino
          </span>
        </Link>
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
                  ? "bg-emerald-800 text-white"
                  : "text-emerald-100 hover:bg-emerald-800/50"
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
