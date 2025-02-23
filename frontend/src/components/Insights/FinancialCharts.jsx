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
  <div className="bg-white rounded-lg shadow-sm border border-emerald-900/10 overflow-hidden">
    <div className="p-5">
      <h3 className="text-base font-semibold text-emerald-900 mb-1">{title}</h3>
      {description && (
        <p className="text-xs text-emerald-600/80 mb-4">{description}</p>
      )}
      <div className="h-[250px]">{children}</div>
    </div>
  </div>
);

const FinancialCharts = ({ data }) => {
  console.log("FinancialCharts received data:", data);

  const renderHeatmap = (plotInfo) => {
    console.log("Rendering heatmap with:", plotInfo);
    if (!plotInfo?.parameters?.values) {
      console.warn("Missing values for heatmap");
      return null;
    }

    const { values, x_axis, y_axis } = plotInfo.parameters;

    // Create chart data from the 2D array
    const chartData = [];
    values.forEach((row, rowIndex) => {
      if (Array.isArray(row)) {
        row.forEach((value, colIndex) => {
          chartData.push({
            x: x_axis[rowIndex],
            y: y_axis[rowIndex],
            value: value,
          });
        });
      }
    });

    console.log("Heatmap chart data:", chartData);

    const maxValue = Math.max(...values.flat());
    const getColor = (value) => {
      const ratio = value / maxValue;
      const r = Math.round(255 * ratio);
      const g = Math.round(100 * (1 - ratio));
      const b = Math.round(100 * (1 - ratio));
      return `rgb(${r},${g},${b})`;
    };

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 30, bottom: 40, left: 40 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              type="category"
              dataKey="x"
              name="Period"
              label={{ value: "Period", position: "bottom", offset: 20 }}
            />
            <YAxis
              type="category"
              dataKey="y"
              name="Category"
              label={{
                value: "Category",
                angle: -90,
                position: "left",
                offset: 20,
              }}
            />
            <Tooltip formatter={(value) => [`£${value}`, "Amount"]} />
            <Scatter data={chartData} fill="#8884d8">
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
    if (!plotInfo?.parameters?.values || !plotInfo?.parameters?.labels) {
      console.warn("Missing values or labels for pie chart");
      return null;
    }

    const chartData = plotInfo.parameters.labels.map((label, idx) => ({
      name: label,
      value: plotInfo.parameters.values[idx],
    }));

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={true}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              nameKey="name"
              label={({ name, value }) => `${name}: £${value.toFixed(2)}`}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
            <Legend verticalAlign="bottom" height={30} />
          </PieChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderLineChart = (plotInfo) => {
    console.log("Rendering line chart with:", plotInfo);
    if (!plotInfo?.parameters?.x_axis || !plotInfo?.parameters?.y_axis) {
      console.warn("Missing axes for line chart");
      return null;
    }

    const chartData = plotInfo.parameters.x_axis.map((x, idx) => ({
      name: x.toString(),
      value: plotInfo.parameters.y_axis[idx],
    }));

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 20, right: 30, bottom: 40, left: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="name"
              label={{
                value: plotInfo.parameters.x_label || "Date",
                position: "bottom",
                offset: 20,
              }}
            />
            <YAxis
              label={{
                value: plotInfo.parameters.y_label || "Value (£)",
                angle: -90,
                position: "left",
                offset: 20,
              }}
            />
            <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
            <Legend verticalAlign="top" height={36} />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#8884d8"
              activeDot={{ r: 8 }}
              name={plotInfo.parameters.title}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderBarChart = (plotInfo) => {
    console.log("Rendering bar chart with:", plotInfo);
    if (!plotInfo?.parameters?.x_axis || !plotInfo?.parameters?.y_axis) {
      console.warn("Missing axes for bar chart");
      return null;
    }

    const chartData = plotInfo.parameters.x_axis.map((x, idx) => ({
      name: x.toString(),
      value: plotInfo.parameters.y_axis[idx],
    }));

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 30, bottom: 40, left: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="name"
              label={{
                value: plotInfo.parameters.x_label || "Date",
                position: "bottom",
                offset: 20,
              }}
            />
            <YAxis
              label={{
                value: plotInfo.parameters.y_label || "Value (£)",
                angle: -90,
                position: "left",
                offset: 20,
              }}
            />
            <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
            <Legend verticalAlign="top" height={36} />
            <Bar
              dataKey="value"
              fill="#8884d8"
              name={plotInfo.parameters.title}
            />
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  const renderScatterPlot = (plotInfo) => {
    console.log("Rendering scatter plot with:", plotInfo);
    if (!plotInfo?.parameters?.x_axis || !plotInfo?.parameters?.y_axis) {
      console.warn("Missing axes for scatter plot");
      return null;
    }

    const chartData = plotInfo.parameters.x_axis.map((x, idx) => ({
      x: x,
      y: plotInfo.parameters.y_axis[idx],
    }));

    return (
      <ChartContainer
        title={plotInfo.parameters.title}
        description={plotInfo.description}
      >
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 30, bottom: 40, left: 40 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="x"
              name={plotInfo.parameters.x_label || "X"}
              label={{
                value: plotInfo.parameters.x_label || "Date",
                position: "bottom",
                offset: 20,
              }}
            />
            <YAxis
              dataKey="y"
              name={plotInfo.parameters.y_label || "Y"}
              label={{
                value: plotInfo.parameters.y_label || "Value (£)",
                angle: -90,
                position: "left",
                offset: 20,
              }}
            />
            <Tooltip formatter={(value) => `£${value.toFixed(2)}`} />
            <Legend verticalAlign="top" height={36} />
            <Scatter
              name={plotInfo.parameters.title}
              data={chartData}
              fill="#8884d8"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </ChartContainer>
    );
  };

  if (!data) {
    console.warn("No data provided to FinancialCharts");
    return null;
  }

  // Group charts by type for better layout
  const chartsByType = Object.entries(data).reduce((acc, [name, info]) => {
    const type = info.type.toLowerCase().replace(/\s+/g, "");
    if (!acc[type]) acc[type] = [];
    acc[type].push({ name, info });
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      {/* Overview charts (pie and bar) */}
      {(chartsByType.piechart || chartsByType.barchart) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {chartsByType.piechart?.map(({ name, info }) => (
            <div key={name}>{renderPieChart(info)}</div>
          ))}
          {chartsByType.barchart?.map(({ name, info }) => (
            <div key={name}>{renderBarChart(info)}</div>
          ))}
        </div>
      )}

      {/* Trend charts (line) */}
      {chartsByType.linechart && (
        <div className="grid grid-cols-1 gap-4">
          {chartsByType.linechart.map(({ name, info }) => (
            <div key={name}>{renderLineChart(info)}</div>
          ))}
        </div>
      )}

      {/* Analysis charts (heatmap and scatter) */}
      {(chartsByType.heatmap || chartsByType.scatterplot) && (
        <div className="grid grid-cols-1 gap-4">
          {chartsByType.heatmap?.map(({ name, info }) => (
            <div key={name}>{renderHeatmap(info)}</div>
          ))}
          {chartsByType.scatterplot?.map(({ name, info }) => (
            <div key={name}>{renderScatterPlot(info)}</div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FinancialCharts;
