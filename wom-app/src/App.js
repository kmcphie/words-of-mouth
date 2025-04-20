import React, { useState, useEffect } from 'react';
import { ReflectiveQuestionGenerator } from './ReflectiveQuestions.js';
import './App.css';

const ReflectiveQuestionApp = () => {
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [questionGenerator] = useState(new ReflectiveQuestionGenerator());
  const [isBrushing, setIsBrushing] = useState(false);
  const [brushingTime, setBrushingTime] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [customQuestion, setCustomQuestion] = useState("");
  const [customCategory, setCustomCategory] = useState("gratitude");
  const [stockSummary, setStockSummary] = useState("");
  
  // Get stocks info
  const fetchStockSummary = async () => {
    try {
      const response = await fetch("http://localhost:5050/api/stock-summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: 1 })
      });
      const data = await response.json();
      setStockSummary(data.stock_summary);
    } catch (error) {
      console.error("Failed to fetch stock summary:", error);
    }
  };
  
  // Generate a new question
  const generateNewQuestion = () => {
    setCurrentQuestion(questionGenerator.generateQuestion());
  };
  
  // Start brushing session
  const startBrushing = () => {
    setIsBrushing(true);
    setBrushingTime(0);
    fetchStockSummary();
    generateNewQuestion();
  };
  
  // End brushing session
  const endBrushing = () => {
    setIsBrushing(false);
  };
  
  // Add custom question
  const addCustomQuestion = () => {
    if (customQuestion.trim() !== "") {
      questionGenerator.addCustomQuestion(customCategory, customQuestion);
      setCustomQuestion("");
      alert("Question added successfully!");
    }
  };
  
  // Timer effect
  useEffect(() => {
    let timer;
    if (isBrushing) {
      timer = setInterval(() => {
        setBrushingTime(prev => {
          const newTime = prev + 1;
          return newTime;
        });
      }, 1000);
    }
    
    return () => clearInterval(timer);
  }, [isBrushing]);
  
  // Audio would be implemented here in a real app
  // This would connect to text-to-speech to read the questions
  
  return (
    <div className="app-container">
      <header>
        <h1>Word of Mouth: Your Talking Toothbrush</h1>
        <p>Take Care of Your Mental and Your Dental Health!</p>
      </header>
      
      <main>
        {!isBrushing ? (
          <div className="setup-section">
            <h2>Evening Reflections</h2>
            <p>Ready to brush your teeth and reflect on your day?</p>
            <button className="primary-button" onClick={startBrushing}>
              Start Brushing
            </button>
            <button 
              className="secondary-button" 
              onClick={() => setShowSettings(!showSettings)}
            >
              {showSettings ? "Hide Settings" : "Show Settings"}
            </button>
            
            {showSettings && (
              <div className="settings-panel">
                <h3>Add Custom Reflection Question</h3>
                <select 
                  value={customCategory}
                  onChange={(e) => setCustomCategory(e.target.value)}
                >
                  {Object.keys(questionGenerator.categories).map(cat => (
                    <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
                  ))}
                </select>
                <input
                  type="text"
                  placeholder="Enter your custom reflection question"
                  value={customQuestion}
                  onChange={(e) => setCustomQuestion(e.target.value)}
                />
                <button className="secondary-button" onClick={addCustomQuestion}>
                  Add Question
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="brushing-section">
            <div className="timer">
              <span>{Math.floor(brushingTime / 60)}:{(brushingTime % 60).toString().padStart(2, '0')}</span>
            </div>

            <div className="stock-card">
              <h2>Stock Market Update</h2>
              <p className="stock-summary">{stockSummary || "Loading stock update..."}</p>
            </div>
            
            <div className="reflection-card">
              <h2>Evening Reflection</h2>
              <p className="question">{currentQuestion}</p>
            </div>
            
            <button className="primary-button" onClick={endBrushing}>
              Finish Brushing
            </button>
          </div>
        )}
      </main>
    </div>
  );
};

export default ReflectiveQuestionApp;
