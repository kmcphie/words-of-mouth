// ReflectiveQuestions.js - Core functionality for generating reflective questions

export class ReflectiveQuestionGenerator {
  constructor() {
    // Define question categories
    this.categories = {
      gratitude: [
        "Think about one thing you're grateful for today.",
        "Reflect on someone who made your day better and why.",
        "Consider a small pleasure you enjoyed today.",
        "What's something you have that many others don't?",
        "Think about an opportunity you had today that you appreciate.",
        "Reflect on a challenge that taught you something valuable.",
        "Consider a relationship in your life you're thankful for.",
        "What aspect of your health are you grateful for today?",
        "Think about a moment of beauty you noticed today.",
        "Reflect on a tool or resource that made your day easier."
      ],
      learning: [
        "What's one thing you learned today?",
        "Think about a mistake that taught you something.",
        "Reflect on advice you received recently that proved useful today.",
        "Consider a skill you improved slightly today.",
        "What's something you realized about yourself today?",
        "Think about something you'd like to learn more about based on today's experiences.",
        "Reflect on how you solved a problem today.",
        "Consider a perspective different from yours that you encountered today.",
        "What surprised you today?",
        "Think about how you might approach tomorrow differently based on today's experiences."
      ],
      achievement: [
        "What's one thing that went better than expected today?",
        "Think about something you accomplished today, however small.",
        "Reflect on a moment you felt proud of yourself today.",
        "Consider a situation you handled well today.",
        "What's a small win you had today?",
        "Think about progress you made toward a goal today.",
        "Reflect on a time you showed strength today.",
        "Consider a moment when you helped someone else today.",
        "What difficulty did you overcome today?",
        "Think about something you did today that your past self would be proud of."
      ],
      wellbeing: [
        "How did you take care of yourself today?",
        "Think about a moment when you felt at peace today.",
        "Reflect on what gave you energy today.",
        "Consider what drained your energy today.",
        "What boundaries did you maintain or need to set?",
        "Think about a moment you felt fully present today.",
        "Reflect on how your body feels right now.",
        "Consider one thing you could do tomorrow to support your wellbeing.",
        "What emotions were most present for you today?",
        "Think about a moment when you showed yourself compassion today."
      ],
      values: [
        "How did you express one of your core values today?",
        "Think about a choice you made today that reflected what matters to you.",
        "Reflect on a moment when you stood up for something important.",
        "Consider how your actions aligned with your priorities today.",
        "What did you say 'no' to today to protect what matters most?",
        "Think about a situation where you compromised or didn't compromise your values.",
        "Reflect on how you might better align your actions with your values tomorrow.",
        "Consider what your actions today say about what's important to you.",
        "When did you feel most like yourself today?",
        "Think about a situation where you wish you had acted differently based on your values."
      ]
    };
    
    // Track question usage to prevent repetition
    this.usedQuestions = new Set();
    this.categoryRotation = Object.keys(this.categories);
    this.categoryIndex = 0;
    
    // Track days for special weekly questions
    this.lastDay = null;
    this.weeklyQuestions = [
      "Looking back on your week, what theme seems to emerge?",
      "What's something you'd like to do differently next week?",
      "Consider one way you've grown this week.",
      "Think about your biggest accomplishment this week.",
      "Reflect on someone who made your week better."
    ];
  }
  
  // Get the next category in rotation
  getNextCategory() {
    const category = this.categoryRotation[this.categoryIndex];
    this.categoryIndex = (this.categoryIndex + 1) % this.categoryRotation.length;
    return category;
  }
  
  // Reset used questions when they've all been used
  resetIfNeeded(category) {
    const questions = this.categories[category];
    const availableQuestions = questions.filter(q => !this.usedQuestions.has(`${category}:${q}`));
    
    if (availableQuestions.length === 0) {
      // Clear used questions for this category
      questions.forEach(q => this.usedQuestions.delete(`${category}:${q}`));
    }
  }
  
  // Check if it's a new day
  checkNewDay() {
    const today = new Date().toDateString();
    if (this.lastDay !== today) {
      this.lastDay = today;
      return true;
    }
    return false;
  }
  
  // Check if it's Sunday evening for weekly reflection
  isWeeklyReflectionTime() {
    const now = new Date();
    return now.getDay() === 0; // Sunday
  }
  
  // Get a weekly reflection question
  getWeeklyQuestion() {
    const index = Math.floor(Math.random() * this.weeklyQuestions.length);
    return this.weeklyQuestions[index];
  }
  
  // Generate a reflection question
  generateQuestion() {
    // Check if it's time for weekly reflection
    if (this.checkNewDay() && this.isWeeklyReflectionTime()) {
      return this.getWeeklyQuestion();
    }
    
    // Get the next category
    const category = this.getNextCategory();
    
    // Make sure there are available questions
    this.resetIfNeeded(category);
    
    // Get questions from the category
    const questions = this.categories[category];
    const availableQuestions = questions.filter(q => !this.usedQuestions.has(`${category}:${q}`));
    
    // Select a random question
    const index = Math.floor(Math.random() * availableQuestions.length);
    const question = availableQuestions[index];
    
    // Mark as used
    this.usedQuestions.add(`${category}:${question}`);
    
    return question;
  }
  
  // Allow adding custom questions
  addCustomQuestion(category, question) {
    if (this.categories[category]) {
      this.categories[category].push(question);
      return true;
    }
    return false;
  }
  
  // Create a new category
  addCategory(categoryName, initialQuestions = []) {
    if (!this.categories[categoryName]) {
      this.categories[categoryName] = initialQuestions;
      this.categoryRotation.push(categoryName);
      return true;
    }
    return false;
  }
}
