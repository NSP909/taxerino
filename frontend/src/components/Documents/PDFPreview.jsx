import {
  XMarkIcon,
  ArrowDownTrayIcon,
  PrinterIcon,
  MagnifyingGlassMinusIcon,
  MagnifyingGlassPlusIcon,
} from "@heroicons/react/24/outline";

export default function PDFPreview({ file, onClose }) {
  if (!file) return null;

  return (
    <div className="fixed inset-0 bg-transparent flex items-center justify-center z-50 p-6">
      <div className="absolute inset-0 bg-black opacity-50" onClick={onClose} />
      <div
        className="bg-[#1a1a1a] w-full max-w-5xl flex flex-col rounded-lg overflow-hidden shadow-2xl relative"
        style={{ height: "80vh" }}
      >
        {/* Top toolbar */}
        <div className="flex items-center justify-between px-4 py-2 bg-[#2a2a2a] text-white border-b border-[#404040]">
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium">{file.name}</span>
            <div className="h-4 w-[1px] bg-gray-600" />
            <span className="text-sm">Page 1 of 1</span>
          </div>

          <div className="flex items-center space-x-2">
            {/* Zoom controls */}
            <div className="flex items-center bg-[#1a1a1a] rounded px-2 py-1">
              <button className="p-1 hover:bg-[#404040] rounded transition-colors">
                <MagnifyingGlassMinusIcon className="h-4 w-4" />
              </button>
              <span className="mx-2 text-sm">100%</span>
              <button className="p-1 hover:bg-[#404040] rounded transition-colors">
                <MagnifyingGlassPlusIcon className="h-4 w-4" />
              </button>
            </div>

            {/* Actions */}
            <button className="p-2 hover:bg-[#404040] rounded transition-colors">
              <PrinterIcon className="h-4 w-4" />
            </button>
            <button className="p-2 hover:bg-[#404040] rounded transition-colors">
              <ArrowDownTrayIcon className="h-4 w-4" />
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-[#404040] rounded transition-colors"
            >
              <XMarkIcon className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* PDF Content */}
        <div className="flex-1 overflow-hidden bg-[#1a1a1a]">
          <iframe
            src={`/api/documents/${file.filename || file.id}#toolbar=0`}
            className="w-full h-full"
            title={`Preview of ${file.name}`}
          />
        </div>
      </div>
    </div>
  );
}
