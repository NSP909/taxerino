import { useState, useEffect } from "react";
import { TaxCache } from "../services/cache";

export function useTaxSummary() {
  const [documentsData, setDocumentsData] = useState(null);
  const [taxSummary, setTaxSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchDocumentsData = async () => {
    try {
      // Check cache first
      const cachedData = TaxCache.get("tax_data");
      if (cachedData) {
        setDocumentsData(cachedData);
        return cachedData;
      }

      const dataResponse = await fetch("/api/documents/data");
      const data = await dataResponse.json();
      setDocumentsData(data);

      // Cache the documents data
      TaxCache.set("tax_data", data);

      // If no documents, set empty status
      if (!data || Object.keys(data).length === 0) {
        setTaxSummary({ status: "empty" });
        return null;
      }

      return data;
    } catch (error) {
      console.error("Failed to fetch documents data:", error);
      return null;
    }
  };

  const generateTaxSummary = async () => {
    try {
      setIsLoading(true);

      // First check if we have documents
      const currentData = await fetchDocumentsData();
      if (!currentData || Object.keys(currentData).length === 0) {
        setTaxSummary({ status: "empty" });
        return;
      }

      // Make API call since we have documents
      const summaryResponse = await fetch("/api/tax-summary");
      const summary = await summaryResponse.json();
      setTaxSummary(summary);

      // Cache the summary
      TaxCache.set("tax_summary", summary);
    } catch (error) {
      console.error("Failed to generate tax summary:", error);
      setTaxSummary({ status: "error", error: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  // Initialize with cached data or fetch new data
  useEffect(() => {
    const initializeData = async () => {
      // Check for cached summary first
      const cachedSummary = TaxCache.get("tax_summary");
      if (cachedSummary) {
        setTaxSummary(cachedSummary);
      }

      // Fetch documents data (this will use cache if available)
      const data = await fetchDocumentsData();

      // If we have documents but no cached summary, generate one
      if (data && Object.keys(data).length > 0 && !cachedSummary) {
        await generateTaxSummary();
      }
    };

    initializeData();
  }, []);

  return {
    documentsData,
    taxSummary,
    isLoading,
    generateTaxSummary,
    refreshData: async (force = false) => {
      if (force) {
        TaxCache.clearTaxData();
      }
      const data = await fetchDocumentsData();
      if (data && Object.keys(data).length > 0) {
        await generateTaxSummary();
      }
    },
  };
}
