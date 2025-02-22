import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Layout from "./components/Layout/Layout";
import LandingPage from "./pages/LandingPage";
import DocumentsPage from "./pages/DocumentsPage";
import "./index.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <Layout>
              <div className="h-full">
                <h1 className="text-2xl font-bold text-gray-900">
                  Welcome to Taxerino
                </h1>
                <p className="mt-2 text-gray-600">
                  Get started by uploading your tax documents
                </p>
              </div>
            </Layout>
          }
        />

        <Route
          path="/documents"
          element={
            <Layout>
              <DocumentsPage />
            </Layout>
          }
        />

        <Route
          path="/chat"
          element={
            <Layout>
              <div className="h-full">
                <h1 className="text-2xl font-bold text-gray-900">
                  Tax Assistant
                </h1>
                <p className="mt-2 text-gray-600">
                  Chat with our AI to get help with your taxes
                </p>
              </div>
            </Layout>
          }
        />

        <Route
          path="/forms"
          element={
            <Layout>
              <div className="h-full">
                <h1 className="text-2xl font-bold text-gray-900">Tax Forms</h1>
                <p className="mt-2 text-gray-600">
                  Fill and manage your tax forms
                </p>
              </div>
            </Layout>
          }
        />

        <Route
          path="/settings"
          element={
            <Layout>
              <div className="h-full">
                <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
                <p className="mt-2 text-gray-600">
                  Manage your account and preferences
                </p>
              </div>
            </Layout>
          }
        />

        {/* Fallback route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
