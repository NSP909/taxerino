import { useEffect, useState } from "react";
import ProgressTracker from "../components/Dashboard/ProgressTracker";
import TaxSummaryPreview from "../components/Dashboard/TaxSummaryPreview";
import { useTaxSummary } from "../hooks/useTaxSummary";

export default function DashboardPage() {
  const [documentsUploaded, setDocumentsUploaded] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  // Get tax data and generation function
  const { documentsData, taxSummary, isLoading, generateTaxSummary } =
    useTaxSummary();

  // Check for uploaded documents
  useEffect(() => {
    let isMounted = true;

    const checkDocuments = async () => {
      try {
        const response = await fetch("/api/documents");
        if (!isMounted) return;

        const documents = await response.json();
        const hasDocuments = documents.length > 0;
        setDocumentsUploaded(hasDocuments);

        if (hasDocuments) {
          setCurrentStep(2);
        }
      } catch (error) {
        console.error("Failed to check documents:", error);
      }
    };

    checkDocuments();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="h-full p-6 space-y-8">
      {/* Header and Progress Tracker */}
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-emerald-900">Welcome Back!</h1>
          <p className="text-emerald-600 mt-1">
            Track your tax filing progress
          </p>
        </div>

        {/* Progress Tracker - Full Width */}
        <ProgressTracker
          documentsUploaded={documentsUploaded}
          currentStep={currentStep}
        />
      </div>

      {/* Tax Summary Preview */}
      <div className="max-w-2xl">
        <TaxSummaryPreview
          taxSummary={taxSummary}
          documentsData={documentsData}
          generateTaxSummary={generateTaxSummary}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
