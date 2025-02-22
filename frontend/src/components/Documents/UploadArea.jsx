import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { DocumentArrowUpIcon } from "@heroicons/react/24/outline";

export default function UploadArea({ onFilesAdded }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      const newFiles = acceptedFiles.map((file) => ({
        file,
        id: Math.random().toString(36).substr(2, 9),
        uploadedAt: new Date().toISOString(),
      }));
      onFilesAdded(newFiles);
    },
    [onFilesAdded]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    multiple: true,
  });

  return (
    <div
      {...getRootProps()}
      className={`h-full border-2 border-dashed rounded-xl flex flex-col items-center justify-center
        transition-colors cursor-pointer
        ${
          isDragActive
            ? "border-indigo-500 bg-indigo-50"
            : "border-gray-300 hover:border-gray-400"
        }`}
    >
      <input {...getInputProps()} />
      <DocumentArrowUpIcon
        className={`h-12 w-12 ${
          isDragActive ? "text-indigo-600" : "text-gray-400"
        }`}
      />
      <p className="mt-4 text-lg font-medium text-gray-700">
        {isDragActive
          ? "Drop your documents here"
          : "Drop your tax documents here"}
      </p>
      <p className="mt-2 text-sm text-gray-500">or click to select files</p>
      <p className="mt-1 text-xs text-gray-400">
        Supports PDF files up to 10MB
      </p>

      {isDragActive && (
        <div className="mt-8 bg-white rounded-lg shadow-sm px-4 py-3">
          <p className="text-sm text-indigo-600 font-medium">
            Ready to upload!
          </p>
        </div>
      )}
    </div>
  );
}
