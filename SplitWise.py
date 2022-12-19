"""
Splitwise
    Requirements
        1. able to create groups and add memebers to it
        2. add or update the expense in the group
        3. settle the expense | ex when A will settle with B in a group then their expenses will become 0

	Identifying the entities and services:

		Tables:
			User
				- userId 		1				2			3
				- name			"shubham"		"shikha"	"random"
				- phoneNumber	8130047792		9981		88743
				- groupId		112				112			112

			Group
				- groupId 		112
				- memberCount	3
				- title			"Goa Trip"

			Expense
				- expenseId  			441		442
				- groupId    			112		112
				- description			cab		food
				- amount				300		500
				- paidByUserId			1		2

			Debt
				- groupId 				112		112		112		112
				- expenseId				441		441		442		442
				- userId 				2		3		1		3
				- owesToUserId 			1		1		2		2
				- amount				100		100		166.66	166.66

		Services:

			SplitWiseService
				+ createGroup(userIds, title)
					> Generate a groupId and add entries in `Group` and `User` table

				+ addMember(groupId, userId)
					> Add entry in `Group` and `User` table

				+ addExpense(groupId, paidByUserId, [splitBetweenUserIdArr], amount, description)
					> lets assume input was >>>> amount = 300, paid by userId 1, splitBetween [2,3]
					> find the member count using the groupId
					> splitAmount = amount / memberCount
					> generate an expense id
					> add an entry in `expense` table
					> add entry in `Debt` table

				+ updateExpenseAmount(expenseId, amount) -> this should also update the amount
					> find groupId using the expenseId
					> find the member count using the groupId
					> splitAmount = amount / memberCount
					> use this expenseId and update the amount in Debt table using the expenseID

				+ updateExpenseDescription(expenseId, desc)

				+ settleExpense(userId1, userId2, groupId, expenseId)
					> use (groupId, userId1, expenseId, userId2 in owesTo) in where clause in `Debt` and update the amount to 0
"""
