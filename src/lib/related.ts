export const relatedMap: Record<string, string[]> = {
  'how-to-raise-your-gpa': ['college-gpa-calculator', 'how-to-study-for-finals'],
  'college-gpa-calculator': ['how-to-raise-your-gpa', 'study-schedule-maker'],
  'how-to-study-for-finals': ['exam-anxiety-tips', 'best-study-techniques-for-college-students'],
  'exam-anxiety-tips': ['how-to-study-for-finals', 'how-to-focus-while-studying'],
  'best-study-techniques-for-college-students': [
    'spaced-repetition-study-method',
    'how-to-take-better-notes-in-college',
  ],
  'spaced-repetition-study-method': [
    'best-study-techniques-for-college-students',
    'how-to-take-better-notes-in-college',
  ],
  'how-to-take-better-notes-in-college': [
    'best-study-techniques-for-college-students',
    'spaced-repetition-study-method',
  ],
  'study-schedule-maker': [
    'how-to-stop-procrastinating-on-homework',
    'how-to-focus-while-studying',
  ],
  'how-to-focus-while-studying': [
    'how-to-stop-procrastinating-on-homework',
    'study-schedule-maker',
  ],
  'how-to-stop-procrastinating-on-homework': [
    'how-to-focus-while-studying',
    'study-schedule-maker',
  ],
};
