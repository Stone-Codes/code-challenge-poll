interface Question {
  id: number;
  text: string;
  visits: number;
}

interface Answer {
  id: number;
  text: string;
  question_id: number;
}
