import { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#8884d8",
  "#82ca9d",
  "#ffc658",
];

const ChartContainer = ({ title, description, children }) => (
  <div className="w-full h-full">{children}</div>
);

const FinancialCharts = ({ data }) => {
  console.log("FinancialCharts received data:", data);

  const renderHeatmap = (plotInfo) => {
    console.log("Rendering heatmap with:", plotInfo);
    if (!plotInfo?.parameters?.data || !plotInfo?.parameters?.names) {
      console.warn("Missing data or names for heatmap");
      return null;
    }

    // Standard heatmap format:
    // data: 2D array [[row1vals], [row2vals]]
    // names: array of labels for both axes
    const { data, names } = plotInfo.parameters;
    const chartData = [];

    // Create chart data from the 2D array
    data.forEach((row, rowIndex) => {
      if (Array.isArray(row)) {
        row.forEach((value, colIndex) => {
          chartData.push({
            x: names[colIndex] || `Column ${colIndex + 1}`,
            y: names[rowIndex + row.length] || `Row ${rowIndex + 1}`,
            value: value || 0,
          });
        });
      }
    });

    // Calculate color based on value ratio
    const maxValue = Math.max(
      ...data.flat().filter((v) => v !== undefined && v !== null)
    );
    const getColor = (value) => {
      const ratio = value / maxValue;
      return `rgb(${Math.round(255 * ratio)},${Math.round(
        100 * (1 - ratio)
      )},${Math.round(100 * (1 - ratio))})`;
    };

    return (
      <ChartContainer
        title={plotInfo.parameters.title || "Chart"}
        description={plotInfo.description || ""}
      >
        <ResponsiveContainer width="100%" height={350}>
          <ScatterChart margin={{ top: 20, right: 30, bottom: 80, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              type="category"
              dataKey="x"
              name="Category"
              label={{
                value: plotInfo.parameters.labels?.[0] || "Category",
                position: "bottom",
                offset: 60,
              }}
              tick={{ angle: -45, textAnchor: "end", dy: 20, fontSize: 12 }}
              height={80}
              stroke="#666"
            />
            <YAxis
              type="category"
              dataKey="y"
              name="Category"
              label={{
                value: plotInfo.parameters.labels?.[1] || "Category",
                angle: -90,
                position: "left",
                offset: 40,
              }}
              stroke="#666"
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => [`$${value.toLocaleString()}`, "Amount"]}
              contentStyle={{
                backgroundColor: "rgba(255, 255, 255, 0.95)",
                borderRadius: "8px",
                border: "1px solid #f0f0f0",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            />
            <Scatter data={chartData}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={getColor(entry.value)}
                  r={20}
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderPieChart = (plotInfo) => {
    console.log("Rendering pie chart with:", plotInfo);
    if (!plotInfo?.parameters?.data || !plotInfo?.parameters?.labels) {
      console.warn("Missing data or labels for pie chart");
      return null;
    }

    // Standard pie chart format:
    // data: array of values
    // labels/names: array of labels
    // colors: array of colors
    const data = Array.isArray(plotInfo.parameters.data)
      ? plotInfo.parameters.data
      : [];
    const labels =
      plotInfo.parameters.labels || plotInfo.parameters.names || [];
    const colors = plotInfo.parameters.colors || [];

    const chartData = labels
      .map((label, idx) => ({
        name: label,
        value: data[idx] || 0,
      }))
      .filter((item) => item.value !== 0);

    return (
      <ChartContainer
        title={plotInfo.parameters.title || "Chart"}
        description={plotInfo.description || ""}
      >
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={true}
              outerRadius={120}
              innerRadius={60}
              fill="#8884d8"
              dataKey="value"
              nameKey="name"
              label={({ name, value, percent }) =>
                `${name}: $${value.toLocaleString()} (${(percent * 100).toFixed(
                  0
                )}%)`
              }
              paddingAngle={2}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={colors[index] || COLORS[index % COLORS.length]}
                  stroke="#fff"
                  strokeWidth={2}
                />
              ))}
            </Pie>
            <Tooltip
              formatter={(value) => `$${value.toLocaleString()}`}
              contentStyle={{
                backgroundColor: "rgba(255, 255, 255, 0.95)",
                borderRadius: "8px",
                border: "1px solid #f0f0f0",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
              formatter={(value) => (
                <span className="text-sm font-medium">{value}</span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderLineChart = (plotInfo) => {
    console.log("Rendering line chart with:", plotInfo);
    if (!plotInfo?.parameters) {
      console.warn("Missing parameters for line chart");
      return null;
    }

    const xAxis = plotInfo.parameters["x axis"] || [];
    const yValues = plotInfo.parameters["y axis"] || [];
    const colors = plotInfo.parameters.colors || [];

    const chartData = xAxis
      .map((x, idx) => ({
        name: x.toString(),
        value: yValues[idx] || 0,
      }))
      .filter((item) => item.value !== 0);

    return (
      <ChartContainer
        title={plotInfo.parameters.title || "Chart"}
        description={plotInfo.description || ""}
      >
        <ResponsiveContainer width="100%" height={350}>
          <LineChart
            data={chartData}
            margin={{ top: 20, right: 30, bottom: 80, left: 60 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="name"
              label={{
                value: plotInfo.parameters.labels?.x || "Category",
                position: "bottom",
                offset: 60,
              }}
              tick={{ angle: -45, textAnchor: "end", dy: 20, fontSize: 12 }}
              height={80}
              stroke="#666"
            />
            <YAxis
              label={{
                value: plotInfo.parameters.labels?.y || "Amount ($)",
                angle: -90,
                position: "left",
                offset: 40,
              }}
              stroke="#666"
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => `$${value.toFixed(2)}`}
              contentStyle={{
                backgroundColor: "rgba(255, 255, 255, 0.9)",
                borderRadius: "8px",
                border: "none",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            />
            <Legend
              verticalAlign="top"
              height={36}
              iconType="circle"
              formatter={(value) => (
                <span className="text-sm font-medium">{value}</span>
              )}
            />
            {chartData.map((_, index) => (
              <Line
                key={`line-${index}`}
                type="monotone"
                dataKey="value"
                stroke={colors[index] || COLORS[index % COLORS.length]}
                activeDot={{ r: 8 }}
                name={
                  plotInfo.parameters.names?.[index] || `Value ${index + 1}`
                }
                strokeWidth={2}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderBarChart = (plotInfo) => {
    console.log("Rendering bar chart with:", plotInfo);
    if (!plotInfo?.parameters) {
      console.warn("Missing parameters for bar chart");
      return null;
    }

    // Standard bar chart format:
    // x axis: array of category labels
    // height: array of values
    // colors: array of colors
    const xAxis = plotInfo.parameters["x axis"] || [];
    const values = plotInfo.parameters.height || [];
    const colors = plotInfo.parameters.colors || [];

    const chartData = xAxis
      .map((x, idx) => ({
        name: x.toString(),
        value: values[idx] || 0,
      }))
      .filter((item) => item.value !== 0);

    return (
      <ChartContainer
        title={plotInfo.parameters.title || "Chart"}
        description={plotInfo.description || ""}
      >
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 30, bottom: 80, left: 60 }}
            barSize={40}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="name"
              label={{
                value: plotInfo.parameters.labels?.[0] || "Category",
                position: "bottom",
                offset: 50,
              }}
              tick={{ angle: -45, textAnchor: "end", dy: 20, fontSize: 12 }}
              height={80}
              stroke="#666"
            />
            <YAxis
              label={{
                value: "Amount ($)",
                angle: -90,
                position: "left",
                offset: 40,
              }}
              stroke="#666"
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => `$${value.toLocaleString()}`}
              contentStyle={{
                backgroundColor: "rgba(255, 255, 255, 0.95)",
                borderRadius: "8px",
                border: "1px solid #f0f0f0",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            />
            <Legend
              verticalAlign="top"
              height={36}
              formatter={(value) => (
                <span className="text-sm font-medium">{value}</span>
              )}
            />
            <Bar dataKey="value" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={colors[index] || COLORS[index % COLORS.length]}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderScatterPlot = (plotInfo) => {
    console.log("Rendering scatter plot with:", plotInfo);
    if (!plotInfo?.parameters) {
      console.warn("Missing parameters for scatter plot");
      return null;
    }

    // Get data arrays
    const xValues = plotInfo.parameters["x axis"] || [];
    const yValues = plotInfo.parameters["y axis"] || [];
    const pointLabels = plotInfo.parameters.labels || [];
    const legendLabels = plotInfo.parameters.legend || [];

    // Create data points
    const chartData = xValues.map((x, idx) => ({
      x,
      y: yValues[idx],
      name: pointLabels[idx],
      category: legendLabels[idx],
    }));

    console.log("Scatter plot data:", chartData);

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart margin={{ top: 20, right: 30, bottom: 80, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              type="number"
              dataKey="x"
              name="Wages"
              label={{ value: "Wages ($)", position: "bottom", offset: 50 }}
              tickFormatter={(value) => `$${value.toLocaleString()}`}
            />
            <YAxis
              type="number"
              dataKey="y"
              name="Tax"
              label={{
                value: "Tax ($)",
                angle: -90,
                position: "left",
                offset: 40,
              }}
              tickFormatter={(value) => `$${value.toLocaleString()}`}
            />
            <Tooltip
              formatter={(value) => `$${value.toLocaleString()}`}
              labelFormatter={(label) => `${label}`}
            />
            <Legend />
            {chartData.map((point, index) => (
              <Scatter
                key={`scatter-${index}`}
                name={point.category}
                data={[point]}
                fill={COLORS[index % COLORS.length]}
              >
                <Cell r={6} />
              </Scatter>
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  if (!data) {
    console.warn("No data provided to FinancialCharts");
    return null;
  }

  // Process the nested data structure
  const processedData = Object.entries(data).reduce((acc, [key, value]) => {
    console.log("Processing chart key:", key);
    console.log("Chart value:", value);

    // Handle both direct and nested key structures
    const chartInfo = value[Object.keys(value)[0]] || value;
    console.log("Chart info:", chartInfo);

    if (chartInfo) {
      acc[key] = {
        type: chartInfo.type,
        description: chartInfo.description,
        parameters: chartInfo.parameters,
      };
    }
    return acc;
  }, {});

  console.log("Processed data:", processedData);

  // Group charts by type
  const chartsByType = Object.entries(processedData).reduce(
    (acc, [name, info]) => {
      const type = info.type.toLowerCase().replace(/\s+/g, "");
      console.log("Chart type after normalization:", type);

      if (!acc[type]) acc[type] = [];
      acc[type].push({ name, info });
      return acc;
    },
    {}
  );

  console.log("Charts by type:", chartsByType);

  return (
    <div className="w-full h-full">
      {/* Render all chart types */}
      {Object.entries(chartsByType).map(([type, charts]) => {
        console.log("Rendering chart type:", type);
        console.log("Charts for this type:", charts);

        return (
          <div key={type} className="h-full">
            {charts.map(({ name, info }) => {
              // Convert type to lowercase and remove spaces for matching
              const normalizedType = type.toLowerCase().replace(/\s+/g, "");
              console.log(
                "Processing chart type:",
                normalizedType,
                "for chart:",
                name
              );

              let ChartComponent = null;
              switch (normalizedType) {
                case "piechart":
                  ChartComponent = renderPieChart(info);
                  break;
                case "barchart":
                  ChartComponent = renderBarChart(info);
                  break;
                case "linechart":
                  ChartComponent = renderLineChart(info);
                  break;
                case "scatterplot":
                  ChartComponent = renderScatterPlot(info);
                  break;
                case "heatmap":
                  ChartComponent = renderHeatmap(info);
                  break;
                default:
                  console.warn("Unknown chart type:", type);
                  break;
              }

              return ChartComponent ? (
                <div key={name} className="h-full">
                  {ChartComponent}
                </div>
              ) : null;
            })}
          </div>
        );
      })}
    </div>
  );
};

export default FinancialCharts;
