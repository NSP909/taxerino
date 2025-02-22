import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Layout from "./components/Layout/Layout";
import LandingPage from "./pages/LandingPage";
import DocumentsPage from "./pages/DocumentsPage";
import ChatPage from "./pages/ChatPage";
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
              <div className="h-full" />
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
              <ChatPage />
            </Layout>
          }
        />

        <Route
          path="/forms"
          element={
            <Layout>
              <div className="h-full" />
            </Layout>
          }
        />

        <Route
          path="/settings"
          element={
            <Layout>
              <div className="h-full" />
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
