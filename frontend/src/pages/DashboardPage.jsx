import { useEffect, useState } from "react";
import ProgressTracker from "../components/Dashboard/ProgressTracker";

export default function DashboardPage() {
  const [documentsUploaded, setDocumentsUploaded] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  // Check for uploaded documents on mount
  useEffect(() => {
    const checkDocuments = async () => {
      try {
        const response = await fetch("/api/documents");
        const documents = await response.json();
        setDocumentsUploaded(documents.length > 0);
        if (documents.length > 0) {
          setCurrentStep(2); // Move to next step if documents exist
        }
      } catch (error) {
        console.error("Failed to check documents:", error);
      }
    };

    checkDocuments();
  }, []);

  return (
    <div className="h-full p-6">
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">Welcome Back!</h1>
          <p className="text-emerald-600 mt-1">
            Track your tax filing progress
          </p>
        </div>

        {/* Progress Tracker */}
        <div className="w-[600px]">
          <ProgressTracker
            documentsUploaded={documentsUploaded}
            currentStep={currentStep}
          />
        </div>
      </div>

      {/* Additional dashboard content can be added here */}
    </div>
  );
}
