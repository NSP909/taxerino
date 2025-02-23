import { useState } from "react";

export function useTaxPlots() {
  const [plotData, setPlotData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPlotData = async (force = false) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetch("/api/tax-plots");
      const data = await response.json();
      console.log("Raw API Response:", data);

      if (data.status === "success" && data.plot_data) {
        // Get the nested data from each category
        const processedData = {};
        Object.entries(data.plot_data).forEach(([category, plots]) => {
          console.log(`Processing category: ${category}`, plots);

          // Skip categories with errors
          if (plots.error) {
            console.warn(
              `Skipping category ${category} due to error:`,
              plots.error
            );
            return;
          }

          Object.entries(plots).forEach(([plotName, plotInfo]) => {
            console.log(`Processing plot: ${plotName}`, plotInfo);

            if (!plotInfo.parameters) {
              console.warn(`Missing parameters for plot ${plotName}`);
              return;
            }

            // Create a new plot info object with standardized parameter names
            const processedPlotInfo = {
              description: plotInfo.description,
              type: plotInfo.type,
              parameters: {
                title: plotInfo.parameters.title,
                colors: plotInfo.parameters.colors,
              },
            };

            // Handle different parameter names for axes
            if (plotInfo.parameters["x axis"]) {
              processedPlotInfo.parameters.x_axis =
                plotInfo.parameters["x axis"];
            } else if (plotInfo.parameters.x_axis) {
              processedPlotInfo.parameters.x_axis = plotInfo.parameters.x_axis;
            }

            if (plotInfo.parameters["y axis"]) {
              processedPlotInfo.parameters.y_axis =
                plotInfo.parameters["y axis"].map(Number);
            } else if (plotInfo.parameters.y_axis) {
              processedPlotInfo.parameters.y_axis =
                plotInfo.parameters.y_axis.map(Number);
            }

            // Handle pie chart data
            if (plotInfo.parameters.data) {
              processedPlotInfo.parameters.values =
                plotInfo.parameters.data.map(Number);
            }

            // Handle labels
            if (plotInfo.parameters.labels) {
              if (Array.isArray(plotInfo.parameters.labels)) {
                processedPlotInfo.parameters.labels =
                  plotInfo.parameters.labels;
              } else if (typeof plotInfo.parameters.labels === "object") {
                processedPlotInfo.parameters.x_label =
                  plotInfo.parameters.labels.x;
                processedPlotInfo.parameters.y_label =
                  plotInfo.parameters.labels.y;
              }
            }

            // Handle heatmap specific data
            if (plotInfo.type.toLowerCase().includes("heatmap")) {
              processedPlotInfo.parameters.values = plotInfo.parameters.data;
              processedPlotInfo.parameters.x_axis = plotInfo.parameters.labels;
              processedPlotInfo.parameters.y_axis = plotInfo.parameters.names;
            }

            // Handle bar chart specific data
            if (plotInfo.type.toLowerCase().includes("bar")) {
              if (plotInfo.parameters.height) {
                processedPlotInfo.parameters.y_axis =
                  plotInfo.parameters.height.map(Number);
              }
            }

            console.log(`Processed plot ${plotName}:`, processedPlotInfo);
            processedData[plotName] = processedPlotInfo;
          });
        });

        console.log("Final processed plot data:", processedData);
        setPlotData(processedData);
        return processedData;
      } else if (data.status === "empty") {
        console.log("No plot data available");
        setPlotData(null);
        return null;
      } else {
        throw new Error(data.error || "Failed to fetch plot data");
      }
    } catch (err) {
      console.error("Error fetching plot data:", err);
      setError(err.message);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    plotData,
    isLoading,
    error,
    refreshPlotData: fetchPlotData,
  };
}
