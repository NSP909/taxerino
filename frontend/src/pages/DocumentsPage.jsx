import { useState, useEffect } from "react";
import UploadArea from "../components/Documents/UploadArea";
import DocumentList from "../components/Documents/DocumentList";
import PDFPreview from "../components/Documents/PDFPreview";
import {
  DocumentMagnifyingGlassIcon,
  ArrowUpTrayIcon,
  DocumentTextIcon,
} from "@heroicons/react/24/outline";
import { TaxCache } from "../services/cache";

// Use relative URL instead of absolute URL
const API_URL = "/api";

export default function DocumentsPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [pendingFiles, setPendingFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [previewFile, setPreviewFile] = useState(null);

  // Fetch existing documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_URL}/documents`); // Simple GET request
      if (!response.ok) throw new Error("Failed to fetch documents");

      const data = await response.json();
      setDocuments(
        data.map((doc) => ({
          id: doc.filename,
          name: doc.filename.substring(16), // Remove timestamp prefix
          size: doc.size,
          uploadedAt: doc.uploadedAt,
          path: doc.path,
          filename: doc.filename, // Keep the original filename for preview
        }))
      );
    } catch (err) {
      setError("Failed to load documents");
      console.error("Error fetching documents:", err);
    }
  };

  const handleFilesAdded = (newFiles) => {
    setPendingFiles(newFiles);
    setError(null);
  };

  const handleUpload = async () => {
    setIsUploading(true);
    setError(null);

    // Upload files one by one
    for (const { file } of pendingFiles) {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${API_URL}/upload`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Failed to upload ${file.name}`);
        }

        // Wait for the response before continuing
        await response.json();
      } catch (err) {
        setError(`Failed to upload ${file.name}`);
        console.error("Upload error:", err);
        setIsUploading(false);
        return; // Stop uploading if there's an error
      }
    }

    // Clear the tax data cache since we have new documents
    TaxCache.clearTaxData();

    // All files uploaded successfully
    await fetchDocuments(); // Refresh the documents list
    setPendingFiles([]); // Clear pending files
    setIsUploading(false);
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    // Pass the complete file object to preview
    setPreviewFile({
      id: file.id,
      name: file.name,
      filename: file.filename,
    });
  };

  const handleClosePreview = () => {
    setPreviewFile(null);
  };

  const handleFileRemove = async (fileId) => {
    // If it's a pending file, just remove it from the pending list
    if (pendingFiles.find((f) => f.id === fileId)) {
      setPendingFiles((prev) => prev.filter((f) => f.id !== fileId));
      return;
    }

    // If it's an uploaded file, delete it from the server
    try {
      const response = await fetch(`${API_URL}/documents/${fileId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Failed to delete file");
      }

      // Clear the tax data cache since we removed a document
      TaxCache.clearTaxData();

      // Remove from UI only after successful server deletion
      setDocuments((prev) => prev.filter((doc) => doc.id !== fileId));

      // Clear selected file if it was deleted
      if (selectedFile?.id === fileId) {
        setSelectedFile(null);
        setPreviewFile(null); // Also close preview if open
      }
    } catch (err) {
      setError(`Failed to delete file: ${err.message}`);
      console.error("Delete error:", err);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Tax Documents</h1>
        <p className="mt-1 text-sm text-gray-500">
          Upload and manage your tax-related documents
        </p>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </div>

      {/* Top section with upload area and pending files */}
      <div className="flex gap-6 h-[300px] mb-8">
        {/* Left side - Drop area */}
        <div className="flex-1">
          <UploadArea onFilesAdded={handleFilesAdded} />
        </div>

        {/* Right side - Pending files and upload button */}
        <div className="flex-1 bg-white rounded-lg shadow-sm p-6 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Selected Documents
            </h2>
            <button
              onClick={handleUpload}
              disabled={pendingFiles.length === 0 || isUploading}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors
                ${
                  pendingFiles.length === 0 || isUploading
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm hover:shadow"
                }`}
            >
              <ArrowUpTrayIcon
                className={`h-4 w-4 mr-2 ${
                  isUploading ? "animate-bounce" : ""
                }`}
              />
              {isUploading ? "Uploading..." : "Upload Files"}
            </button>
          </div>

          <div className="flex-1 overflow-auto">
            {pendingFiles.length > 0 ? (
              <div className="space-y-2">
                {pendingFiles.map(({ file, id }) => (
                  <div
                    key={id}
                    className="bg-white border border-gray-200 rounded-lg p-3 flex items-center justify-between hover:border-gray-300 transition-colors"
                  >
                    <div className="flex items-center space-x-3 flex-1 min-w-0">
                      <DocumentTextIcon className="h-6 w-6 text-gray-400" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {file.name}
                        </p>
                        <p className="text-xs text-gray-500 mt-0.5">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                    <span className="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded">
                      Ready to upload
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center text-gray-500">
                <DocumentMagnifyingGlassIcon className="h-12 w-12 mb-3" />
                <p>No documents selected</p>
                <p className="text-sm">Drop files on the left to select them</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom section - Uploaded documents */}
      <div className="flex-1 bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Uploaded Documents
        </h2>
        {documents.length > 0 ? (
          <DocumentList
            documents={documents}
            selectedFile={selectedFile}
            onFileSelect={handleFileSelect}
            onFileRemove={handleFileRemove}
          />
        ) : (
          <div className="text-center py-12 text-gray-500">
            <DocumentMagnifyingGlassIcon className="h-12 w-12 mx-auto mb-3" />
            <p>No documents uploaded yet</p>
            <p className="text-sm">Upload some documents to see them here</p>
          </div>
        )}
      </div>

      {/* PDF Preview Modal */}
      {previewFile && (
        <PDFPreview file={previewFile} onClose={handleClosePreview} />
      )}
    </div>
  );
}
