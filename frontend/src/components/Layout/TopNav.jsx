import { BellIcon } from "@heroicons/react/24/outline";

export default function TopNav() {
  return (
    <div className="h-16 bg-white border-b border-gray-200">
      <div className="h-full px-4 flex items-center justify-between">
        <div className="flex-1" /> {/* Spacer */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="p-2 text-gray-400 hover:text-gray-500 rounded-full hover:bg-gray-50">
            <BellIcon className="h-6 w-6" />
          </button>

          {/* Profile */}
          <div className="flex items-center space-x-3">
            <div className="flex flex-col items-end">
              <span className="text-sm font-medium text-gray-700">
                John Doe
              </span>
              <span className="text-xs text-gray-500">john@example.com</span>
            </div>
            <button className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center">
              <span className="text-sm font-medium text-gray-600">JD</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
