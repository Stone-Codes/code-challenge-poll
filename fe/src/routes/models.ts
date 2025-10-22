interface Question {
	id: number;
	text: string;
}

interface Answer {
	id: number;
	text: string;
	question_id: number;
}
