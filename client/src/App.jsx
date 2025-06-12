import React, { useState } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'react-hot-toast';

export default function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return toast.error("📁 Please select an Excel file!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData);
      toast.success(res.data.message);
    } catch (error) {
      toast.error("❌ Upload failed! Try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-pink-100 flex items-center justify-center p-4">
      <Toaster position="top-right" />
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4 text-center text-pink-600">
          🎉 Birthday Mailer
        </h1>
        <input
          type="file"
          accept=".xlsx"
          onChange={handleFileChange}
          className="mb-4 block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-full file:bg-pink-100 file:text-pink-700 hover:file:bg-pink-200"
        />
        <button
          onClick={handleUpload}
          className="w-full bg-pink-600 text-white font-semibold py-2 rounded-xl hover:bg-pink-700 transition duration-300"
        >
          Upload Excel File
        </button>
      </div>
    </div>
  );
}
