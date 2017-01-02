var config = require('./config');
var ESO_FACTS = require(./fact_bank);

/**
 * App ID for the skill
 */
var APP_ID = config.appId;


/**
 * The AlexaSkill prototype and helper functions
 */
var AlexaSkill = require('./AlexaSkill');

/**
 * FactsForElderScrolls is a child of AlexaSkill.
 * To read more about inheritance in JavaScript, see the link below.
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Introduction_to_Object-Oriented_JavaScript#Inheritance
 */
var FactsForElderScrolls = function () {
	AlexaSkill.call(this, APP_ID);
};

//Extend AlexaSkill
FactsForElderScrolls.prototype = Object.create(AlexaSkill.prototype);
FactsForElderScrolls.prototype.constructor = FactsForElderScrolls;

FactsForElderScrolls.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
	console.log("FactsForElderScrolls onSessionStarted requestId: " + sessionStartedRequest.requestId
			+ ", sessionId: " + session.sessionId);
	// any initialization logic goes here
};

FactsForElderScrolls.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
	console.log("FactsForElderScrolls onLaunch requestId: " + launchRequest.requestId + ", sessionId: " + session.sessionId);
	handleNewFactRequest(response);
};

/**
 * Overridden to show that a subclass can override this function to teardown session state.
 */
FactsForElderScrolls.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
	console.log("FactsForElderScrolls onSessionEnded requestId: " + sessionEndedRequest.requestId
			+ ", sessionId: " + session.sessionId);
	// any cleanup logic goes here
};

FactsForElderScrolls.prototype.intentHandlers = {
		"GetNewFactIntent": function (intent, session, response) {
			handleNewFactRequest(response);
		},

		"AMAZON.HelpIntent": function (intent, session, response) {
			response.ask("You can ask Facts for Elder Scrolls tell me a Elder Scrolls fact, or, you can say exit... What can I help you with?", "What can I help you with?");
		},

		"AMAZON.StopIntent": function (intent, session, response) {
			var speechOutput = "Goodbye";
			response.tell(speechOutput);
		},

		"AMAZON.CancelIntent": function (intent, session, response) {
			var speechOutput = "Goodbye";
			response.tell(speechOutput);
		}
};

/**
 * Gets a random new fact from the list and returns to the user.
 */
function handleNewFactRequest(response) {
	// Get a random Elder Scrolls fact from the Elder Scrolls facts list
	var factIndex = Math.floor(Math.random() * ESO_FACTS.length);
	var fact = ESO_FACTS[factIndex];

	// Create speech output
	var speechOutput = "Here's your Elder Scrolls fact: " + "Did you know " + fact;

	response.tellWithCard(speechOutput, "FactsForElderScrolls", speechOutput);
}

//Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
	// Create an instance of the FactsForElderScrolls skill.
	var factsForElderScrolls = new FactsForElderScrolls();
	factsForElderScrolls.execute(event, context);
};

