const API_URL = "/api";

export const AnalysisService = {
  async getTaxSummary() {
    try {
      const response = await fetch(`${API_URL}/cache/tax_summary.json`);
      if (!response.ok) throw new Error("Failed to fetch tax summary");
      return await response.json();
    } catch (error) {
      console.error("Error fetching tax summary:", error);
      throw error;
    }
  },

  async getTaxPlots() {
    try {
      const response = await fetch(`${API_URL}/cache/tax_plots.json`);
      if (!response.ok) throw new Error("Failed to fetch tax plots");
      return await response.json();
    } catch (error) {
      console.error("Error fetching tax plots:", error);
      throw error;
    }
  },

  async getBenfordAnalysis() {
    try {
      const response = await fetch(`${API_URL}/cache/benford.json`);
      if (!response.ok) throw new Error("Failed to fetch Benford analysis");
      return await response.json();
    } catch (error) {
      console.error("Error fetching Benford analysis:", error);
      throw error;
    }
  },

  async getAnomalies() {
    try {
      const response = await fetch(`${API_URL}/cache/anomalies.json`);
      if (!response.ok) throw new Error("Failed to fetch anomalies");
      return await response.json();
    } catch (error) {
      console.error("Error fetching anomalies:", error);
      throw error;
    }
  },
};
