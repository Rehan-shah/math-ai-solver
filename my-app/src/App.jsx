import React, { useState } from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';

const MathApp = () => {
  const [question, setQuestion] = useState('');
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showVideo, setShowVideo] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(false);
    setShowVideo(false);

    try {
      const response = await fetch(`http://localhost:8000?problem=${encodeURIComponent(question)}`);
      const data = await response.json();
      console.log(data);
      if (data.code === 0) {
        setShowVideo(true);
      } else {
        setError(true);
      }
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center p-4">
    <p className='absolute z-10 bottom-0 mb-10 text-white '>Made by <a className='underline hover:font-bold' href="https://github.com/Rehan-shah">Rehan Shah</a></p>
      <div className="relative bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-2xl p-8 w-full max-w-md shadow-xl border border-white border-opacity-20 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-white opacity-5 z-0"></div>
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-6 text-white text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
            Minute Math
          </h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter your math question"
                className="w-full p-3 rounded-lg bg-white bg-opacity-20 placeholder-gray-300 text-white border border-white border-opacity-30 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition duration-300"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white p-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-opacity-50 shadow-lg"
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="animate-spin mx-auto" />
              ) : (
                'Submit'
              )}
            </button>
          </form>
          {error && (
            <div className="mt-4 p-3 bg-red-100 bg-opacity-30 border border-red-400 border-opacity-50 text-red-100 rounded-lg flex items-center animate-fade-in-down">
              <AlertCircle className="mr-2 flex-shrink-0" />
              <span>An error occurred. Please try again.</span>
            </div>
          )}
          {showVideo && (
            <div className="mt-4 animate-fade-in">
              <video controls className="w-full rounded-lg shadow-lg">
                <source src="./final_video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )
          }
        </div>

      </div>
    </div>

  );
};

export default MathApp;
