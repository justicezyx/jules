package com.example.aichatapp.service

import kotlinx.coroutines.delay

class MockAiService {

    suspend fun generateResponse(userInput: String): String {
        delay(500) // Simulate processing time

        val lowerInput = userInput.lowercase()

        return when {
            "hello" in lowerInput || "hi" in lowerInput -> "Hi there! How can I assist you today?"
            "how are you" in lowerInput -> "I'm doing well, thank you for asking!"
            "bye" in lowerInput || "goodbye" in lowerInput -> "Goodbye! Have a great day!"
            // The instruction mentioned: "For any other input, return "I'm a simple mock AI. I received: '$userInput'"
            // And "Add a default response if no rules match: 'Sorry, I didn't quite understand that.'"
            // The following logic attempts to reconcile this. If a specific "echo" command is desired, it could be added.
            // Otherwise, the more general "didn't understand" is used as the fallback.
            // For now, I will prioritize "Sorry, I didn't quite understand that." as the ultimate fallback.
            // If an explicit echo for "any other input" is needed as a distinct rule, it should be added above the final else.
            else -> "Sorry, I didn't quite understand that."
        }
    }
}
