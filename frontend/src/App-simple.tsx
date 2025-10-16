import { useState } from 'react';

export default function App() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-background text-foreground p-4 md:p-8 lg:p-12">
        <div className="max-w-[1600px] mx-auto space-y-6">
          
          <h1 className="text-4xl font-bold text-center mb-8">
            GameDay Predictor
          </h1>
          
          <p className="text-center text-muted-foreground">
            Your Figma UI is now working! 🎉
          </p>
          
          <div className="text-center">
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
            >
              Toggle {darkMode ? 'Light' : 'Dark'} Mode
            </button>
          </div>
          
        </div>
      </div>
    </div>
  );
}