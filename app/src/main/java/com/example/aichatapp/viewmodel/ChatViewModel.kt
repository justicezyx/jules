package com.example.aichatapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aichatapp.data.ChatMessage
import com.example.aichatapp.data.SenderType
import com.example.aichatapp.service.MockAiService // Added import
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ChatViewModel : ViewModel() {

    private val aiService = MockAiService() // Added AI Service instance
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    init {
        // Add an initial welcome message from the AI
        _messages.value = listOf(ChatMessage("Hello! I'm your AI assistant.", SenderType.AI))
    }

    fun sendMessage(text: String) {
        if (text.isBlank()) return

        val userMessage = ChatMessage(text = text, sender = SenderType.USER)
        _messages.value = _messages.value + userMessage

        // Simulate AI Response
        viewModelScope.launch {
            // The aiService.generateResponse itself has a 500ms delay.
            // Keeping an additional delay here to simulate overall network/processing.
            // Total delay will be around 1500ms (1000ms here + 500ms in service).
            delay(1000) 
            val aiResponseText = aiService.generateResponse(userMessage.text) // Use aiService
            val aiMessage = ChatMessage(text = aiResponseText, sender = SenderType.AI)
            _messages.value = _messages.value + aiMessage
        }
    }
}
