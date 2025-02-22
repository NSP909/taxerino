import { Link } from "react-router-dom";
import {
  ArrowRightIcon,
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/outline";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white flex flex-col items-center justify-center p-4">
      <div className="text-center max-w-3xl">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Simplify Your Tax Filing Journey
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          Upload your documents, chat with our AI assistant, and complete your
          taxes with confidence.
        </p>

        <Link
          to="/dashboard"
          className="inline-flex items-center px-8 py-4 bg-indigo-600 text-white font-medium rounded-xl
                   hover:bg-indigo-700 transition-colors shadow-lg hover:shadow-xl"
        >
          Get Started
          <ArrowRightIcon className="ml-2 h-5 w-5" />
        </Link>
      </div>

      {/* Features */}
      <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl w-full">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="h-12 w-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <DocumentTextIcon className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Easy Document Upload</h3>
          <p className="text-gray-600">
            Securely upload and manage all your tax-related documents in one
            place.
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="h-12 w-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <ChatBubbleLeftRightIcon className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">AI Assistant</h3>
          <p className="text-gray-600">
            Get instant answers to your tax questions from our intelligent
            assistant.
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="h-12 w-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <ShieldCheckIcon className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Secure & Reliable</h3>
          <p className="text-gray-600">
            Your data is protected with enterprise-grade security measures.
          </p>
        </div>
      </div>
    </div>
  );
}
