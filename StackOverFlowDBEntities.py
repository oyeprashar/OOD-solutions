"""
Design stack overflow DB entities

Requirements:
	- A user register themselves
	- A user can ask a question
	- A user can answer a question
	- A user can search a questions based on tags associated to a question

Identifying the entities and services:

	Database models

		1. User
			- user_id  --> primary_key and foreign_key
			- first_name
			- last_name
			- email_address

		2. Question
			- question_id --> primary_key
			- user_id --> foreign_key
			- description
			- topic_tag

		3. Answer
			- answer_id
			- questions_id
			- user_id
			- description

	- We can access questions asked by a user by using their user_id as foreign key and accessing `Question` table
	- We can access all the answers of a questions by using the question_id as foreign key and accessing `Answer` table

Services:

	StackOverFlowService
		+ registerUser
		+ answerQuestion
		+ askQuestion
		+ findQuestionsByTag

"""
