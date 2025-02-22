import {
  DocumentTextIcon,
  XMarkIcon,
  EyeIcon,
} from "@heroicons/react/24/outline";

export default function DocumentList({
  documents,
  selectedFile,
  onFileSelect,
  onFileRemove,
}) {
  return (
    <div className="space-y-4">
      {documents.map((doc) => {
        const isSelected = selectedFile?.id === doc.id;
        return (
          <div
            key={doc.id}
            className={`w-full bg-white border rounded-lg overflow-hidden transition-shadow hover:shadow-md
              ${isSelected ? "ring-2 ring-indigo-500" : "border-gray-200"}`}
          >
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3 flex-1">
                  <DocumentTextIcon
                    className={`h-8 w-8 flex-shrink-0 ${
                      isSelected ? "text-indigo-600" : "text-gray-400"
                    }`}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {doc.name}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {(doc.size / 1024 / 1024).toFixed(2)} MB •{" "}
                      {new Date(doc.uploadedAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => onFileSelect(doc)}
                    className="flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 hover:text-indigo-700 
                      bg-indigo-50 rounded-md hover:bg-indigo-100"
                  >
                    <EyeIcon className="h-4 w-4 mr-1" />
                    Preview
                  </button>
                  <button
                    onClick={() => onFileRemove(doc.id)}
                    className="p-1.5 text-gray-400 hover:text-gray-500 rounded-full hover:bg-gray-100"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
