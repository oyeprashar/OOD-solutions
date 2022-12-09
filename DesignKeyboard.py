"""
Design a virtual keyboard

1. Requirement gathering
	- A keyboard on the screen
	- User can press buttons and write

2. Identifying the entities and services

	Entities:
		1. Keyboard
			- language_code
			- keys
			- model_id

		2. Key <-- factory pattern can be used to get all keys of a language
			- id
			+ pressed() // This will be overloaded

		3. CharKey inherits Key class
			- char
			+ function() <- output the character

		4. SpecialKey inherits Key class # special function keys remain same for all the keys board
			+ function() <- delete, blank space, shift

	Database:
		Table name: lang-keys # here we use language code to pick all the keys
		Attributes:
			- language_code : en, en
			- switch_id : 1, 2
			- lower_case_character: a, b
			- upper_case_character: A, B

		Table name: special-keys # here we use the switch ids to pick all the special keys
		Attributes:
			- model_id : 97415
			- switch_id : 99
			- functionality: backspace

	Service:
		KeyboardService
			+ createKeyboard(langCode, modelId)
			+ pressKey(switchId)
			
3. Design
4. Refine



"""